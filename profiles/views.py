from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from .models import JobSeekerProfile
from .forms import JobSeekerProfileForm
from applications.models import Application


def jobseeker_profile_view(request, username):
    """View a job seeker's public profile."""
    user = get_object_or_404(User, username=username)
    profile = get_object_or_404(JobSeekerProfile, user=user)

    context = {"profile_user": user, "profile": profile}

    # Show application history only to the owner or employers
    if request.user.is_authenticated:
        if request.user == user:
            context["applications"] = Application.objects.filter(
                job_seeker=profile
            ).select_related("job", "job__company").order_by("-applied_at")
        elif request.user.profile.role == "employer":
            context["applications"] = Application.objects.filter(
                job_seeker=profile, job__company__owner=request.user
            ).select_related("job").order_by("-applied_at")

    return render(request, "profiles/jobseeker_profile.html", context)


@login_required
def jobseeker_profile_edit(request):
    """Edit the logged-in user's job seeker profile."""
    if request.user.profile.role != "job_seeker":
        messages.error(request, "Only job seekers can edit this profile.")
        return redirect("dashboard:dashboard")

    profile, created = JobSeekerProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect("profiles:jobseeker_profile", username=request.user.username)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobSeekerProfileForm(instance=profile, user=request.user)

    return render(request, "profiles/jobseeker_profile_form.html", {
        "form": form,
        "profile": profile,
    })


@login_required
def jobseeker_profile_create(request):
    """Create a job seeker profile."""
    if request.user.profile.role != "job_seeker":
        messages.error(request, "Only job seekers can create this profile.")
        return redirect("dashboard:dashboard")

    if JobSeekerProfile.objects.filter(user=request.user).exists():
        messages.info(request, "You already have a profile. You can edit it instead.")
        return redirect("profiles:jobseeker_profile_edit")

    if request.method == "POST":
        form = JobSeekerProfileForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been created!")
            return redirect("profiles:jobseeker_profile", username=request.user.username)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = JobSeekerProfileForm(user=request.user)

    return render(request, "profiles/jobseeker_profile_form.html", {
        "form": form,
        "creating": True,
    })
