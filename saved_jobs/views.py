from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import SavedJob
from .forms import SaveJobForm, SavedJobBulkActionForm
from jobs.models import Job


@login_required
def saved_job_list(request):
    """List all saved jobs for the logged-in job seeker."""
    saved_jobs = SavedJob.objects.filter(
        job_seeker__user=request.user
    ).select_related("job", "job__company").order_by("-created_at")

    bulk_form = SavedJobBulkActionForm()

    return render(request, "saved_jobs/saved_job_list.html", {
        "saved_jobs": saved_jobs,
        "bulk_form": bulk_form,
    })


@login_required
@require_POST
def save_job(request, job_pk):
    """Save/unsave a job (toggle)."""
    if request.user.profile.role != "job_seeker":
        messages.error(request, "Only job seekers can save jobs.")
        return redirect("jobs:job_detail", pk=job_pk)

    job = get_object_or_404(Job, pk=job_pk)
    job_seeker = request.user.profile.jobseekerprofile

    saved, created = SavedJob.objects.get_or_create(
        job_seeker=job_seeker, job=job
    )

    if not created:
        saved.delete()
        status = "unsaved"
        messages.info(request, f"'{job.title}' removed from saved jobs.")
    else:
        status = "saved"
        messages.success(request, f"'{job.title}' saved!")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"status": status, "job_pk": job.pk})

    return redirect("jobs:job_detail", pk=job_pk)


@login_required
@require_POST
def unsave_job(request, pk):
    """Remove a specific saved job."""
    saved_job = get_object_or_404(
        SavedJob, pk=pk, job_seeker__user=request.user
    )
    job_title = saved_job.job.title
    saved_job.delete()
    messages.info(request, f"'{job_title}' removed from saved jobs.")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"status": "ok", "pk": pk})

    return redirect("saved_jobs:saved_job_list")


@login_required
@require_POST
def bulk_unsave(request):
    """Bulk remove saved jobs."""
    form = SavedJobBulkActionForm(request.POST)
    if form.is_valid():
        ids = form.cleaned_data["saved_job_ids"]
        action = form.cleaned_data["action"]

        if action == "unsave":
            deleted = SavedJob.objects.filter(
                pk__in=ids, job_seeker__user=request.user
            ).delete()
            messages.success(request, f"{deleted[0]} saved job(s) removed.")

    return redirect("saved_jobs:saved_job_list")
