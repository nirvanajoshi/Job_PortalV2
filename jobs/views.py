from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Job
from .forms import JobForm, JobStatusForm
from companies.models import Company
from applications.models import Application
from saved_jobs.models import SavedJob


def job_list(request):
    """List all published jobs."""
    jobs = Job.objects.filter(status="published").select_related("company")
    return render(request, "jobs/job_list.html", {"jobs": jobs})


def job_detail(request, pk):
    """View a specific job's details."""
    job = get_object_or_404(
        Job.objects.select_related("company"), pk=pk
    )
    context = {"job": job}

    # Check if the logged-in job seeker has already applied
    if request.user.is_authenticated and request.user.profile.role == "job_seeker":
        job_seeker = request.user.profile.jobseekerprofile
        context["has_applied"] = Application.objects.filter(
            job_seeker=job_seeker, job=job
        ).exists()
        context["saved"] = SavedJob.objects.filter(
            job_seeker=job_seeker, job=job
        ).exists()

    # Employer can see application count for their own jobs
    if request.user.is_authenticated and request.user.profile.role == "employer":
        if job.company.owner == request.user:
            context["application_count"] = Application.objects.filter(job=job).count()
            context["status_form"] = JobStatusForm(instance=job)

    return render(request, "jobs/job_detail.html", context)


@login_required
def job_create(request):
    """Create a new job (employer only)."""
    if request.user.profile.role != "employer":
        messages.error(request, "Only employers can create jobs.")
        return redirect("dashboard:dashboard")

    try:
        company = Company.objects.get(owner=request.user)
    except Company.DoesNotExist:
        messages.warning(request, "Please create a company profile first.")
        return redirect("companies:company_create")

    if request.method == "POST":
        form = JobForm(request.POST, user=request.user)
        if form.is_valid():
            job = form.save()
            messages.success(request, f"Job '{job.title}' has been created!")
            return redirect("jobs:job_detail", pk=job.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobForm(user=request.user)

    return render(request, "jobs/job_form.html", {"form": form, "action": "Create"})


@login_required
def job_update(request, pk):
    """Update a job (owner employer only)."""
    job = get_object_or_404(Job, pk=pk)

    if job.company.owner != request.user:
        raise PermissionDenied("You do not have permission to edit this job.")

    if request.method == "POST":
        form = JobForm(request.POST, instance=job, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Job '{job.title}' has been updated!")
            return redirect("jobs:job_detail", pk=job.pk)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobForm(instance=job, user=request.user)

    return render(request, "jobs/job_form.html", {"form": form, "job": job, "action": "Edit"})


@login_required
def job_delete(request, pk):
    """Delete a job (owner employer only)."""
    job = get_object_or_404(Job, pk=pk)

    if job.company.owner != request.user:
        raise PermissionDenied("You do not have permission to delete this job.")

    if request.method == "POST":
        job_title = job.title
        job.delete()
        messages.info(request, f"Job '{job_title}' has been deleted.")
        return redirect("jobs:job_list")

    return render(request, "jobs/job_confirm_delete.html", {"job": job})


@login_required
def update_job_status(request, pk):
    """Update job status (owner employer only)."""
    job = get_object_or_404(Job, pk=pk)

    if job.company.owner != request.user:
        raise PermissionDenied("You do not have permission to update this job.")

    if request.method == "POST":
        form = JobStatusForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, f"Job status updated to {job.get_status_display()}.")

    return redirect("jobs:job_detail", pk=job.pk)
