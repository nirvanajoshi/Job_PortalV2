from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Application
from .forms import ApplicationForm, ApplicationStatusForm
from jobs.models import Job
from companies.models import Company


@login_required
def application_list(request):
    """List all applications for the logged-in job seeker."""
    applications = Application.objects.filter(
        job_seeker__user=request.user
    ).select_related("job", "job__company")
    return render(request, "applications/application_list.html", {"applications": applications})


@login_required
def application_detail(request, pk):
    """View a specific application's details."""
    application = get_object_or_404(
        Application.objects.select_related("job", "job__company", "job_seeker__user"),
        pk=pk,
    )

    # Job seeker can only see their own applications
    if request.user.profile.role == "job_seeker" and application.job_seeker.user != request.user:
        raise PermissionDenied("You do not have permission to view this application.")

    # Employer can only see applications for their company's jobs
    if request.user.profile.role == "employer" and application.job.company.owner != request.user:
        raise PermissionDenied("You do not have permission to view this application.")

    status_form = ApplicationStatusForm(instance=application) if request.user.profile.role == "employer" else None
    return render(request, "applications/application_detail.html", {
        "application": application,
        "status_form": status_form,
    })


@login_required
def apply_job(request, job_pk):
    """Apply to a specific job."""
    job = get_object_or_404(Job, pk=job_pk, status="published")

    # Check if user is a job seeker
    if request.user.profile.role != "job_seeker":
        messages.error(request, "Only job seekers can apply for jobs.")
        return redirect("jobs:job_detail", pk=job_pk)

    # Check if already applied
    job_seeker = request.user.profile.jobseekerprofile
    if Application.objects.filter(job_seeker=job_seeker, job=job).exists():
        messages.warning(request, "You have already applied to this job.")
        return redirect("applications:application_detail", pk=Application.objects.get(job_seeker=job_seeker, job=job).pk)

    if request.method == "POST":
        form = ApplicationForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            application = form.save(commit=False)
            application.job_seeker = job_seeker
            application.job = job
            application.save()
            messages.success(request, f"Your application for {job.title} has been submitted!")
            return redirect("applications:application_detail", pk=application.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ApplicationForm(user=request.user, initial={"job": job})

    return render(request, "applications/apply_job.html", {"form": form, "job": job})


@login_required
def withdraw_application(request, pk):
    """Withdraw a job application."""
    application = get_object_or_404(
        Application, pk=pk, job_seeker__user=request.user
    )

    if request.method == "POST":
        application.status = "withdrawn"
        application.save()
        messages.info(request, f"Your application for {application.job.title} has been withdrawn.")
    return redirect("applications:application_list")


@login_required
def employer_applications(request):
    """List all applications for jobs owned by the logged-in employer's company."""
    try:
        company = Company.objects.get(owner=request.user)
    except Company.DoesNotExist:
        messages.error(request, "You do not have a company profile.")
        return redirect("dashboard:dashboard")

    applications = Application.objects.filter(
        job__company=company
    ).select_related("job_seeker__user", "job")

    status_filter = request.GET.get("status", "")
    if status_filter:
        applications = applications.filter(status=status_filter)

    return render(request, "applications/employer_applications.html", {
        "applications": applications,
        "status_choices": Application.STATUS_CHOICES,
        "current_status": status_filter,
    })


@login_required
def update_application_status(request, pk):
    """Update the status of an application (employer only)."""
    application = get_object_or_404(
        Application.objects.select_related("job__company"),
        pk=pk,
        job__company__owner=request.user,
    )

    if request.method == "POST":
        form = ApplicationStatusForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, f"Application status updated to {application.get_status_display()}.")
        else:
            messages.error(request, "Invalid status.")

    return redirect("applications:application_detail", pk=application.pk)
