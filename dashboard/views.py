from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from jobs.models import Job
from companies.models import Company
from applications.models import Application
from .forms import JobSearchForm, CompanySearchForm, ApplicationFilterForm


@login_required
def dashboard(request):
    """Main dashboard - shows different content based on user role."""
    user = request.user
    role = user.profile.role
    context = {"role": role}

    if role == "employer":
        try:
            company = Company.objects.get(owner=user)
            recent_jobs = Job.objects.filter(company=company).order_by("-created_at")[:5]
            recent_applications = Application.objects.filter(
                job__company=company
            ).select_related("job_seeker__user", "job").order_by("-applied_at")[:5]
            total_applications = Application.objects.filter(job__company=company).count()
            context.update({
                "company": company,
                "recent_jobs": recent_jobs,
                "recent_applications": recent_applications,
                "total_jobs": recent_jobs.count(),
                "total_applications": total_applications,
            })
        except Company.DoesNotExist:
            context["company"] = None

    elif role == "job_seeker":
        applications = Application.objects.filter(
            job_seeker__user=user
        ).select_related("job", "job__company").order_by("-applied_at")
        saved_jobs = Job.objects.filter(savedjob__user=user)[:5]
        recommended_jobs = Job.objects.filter(
            status="published"
        ).order_by("-created_at")[:5]
        context.update({
            "recent_applications": applications[:5],
            "total_applications": applications.count(),
            "saved_jobs": saved_jobs,
            "recommended_jobs": recommended_jobs,
        })

    else:
        # Admin or other roles
        total_jobs = Job.objects.count()
        total_companies = Company.objects.count()
        total_applications = Application.objects.count()
        context.update({
            "total_jobs": total_jobs,
            "total_companies": total_companies,
            "total_applications": total_applications,
        })

    return render(request, "dashboard/dashboard.html", context)


def job_search(request):
    """Search and filter jobs."""
    form = JobSearchForm(request.GET or None)
    jobs = Job.objects.filter(status="published").select_related("company")

    if form.is_valid():
        keyword = form.cleaned_data.get("keyword")
        location = form.cleaned_data.get("location")
        job_type = form.cleaned_data.get("job_type")
        work_mode = form.cleaned_data.get("work_mode")
        experience_level = form.cleaned_data.get("experience_level")
        salary_min = form.cleaned_data.get("salary_min")
        salary_max = form.cleaned_data.get("salary_max")

        if keyword:
            jobs = jobs.filter(
                Q(title__icontains=keyword)
                | Q(description__icontains=keyword)
                | Q(skills_required__icontains=keyword)
                | Q(company__name__icontains=keyword)
            )
        if location:
            jobs = jobs.filter(location__icontains=location)
        if job_type:
            jobs = jobs.filter(job_type=job_type)
        if work_mode:
            jobs = jobs.filter(work_mode=work_mode)
        if experience_level:
            jobs = jobs.filter(experience_level=experience_level)
        if salary_min:
            jobs = jobs.filter(salary_min__gte=salary_min)
        if salary_max:
            jobs = jobs.filter(salary_max__lte=salary_max)

    return render(request, "dashboard/job_search.html", {
        "form": form,
        "jobs": jobs,
    })


def company_search(request):
    """Search and filter companies."""
    form = CompanySearchForm(request.GET or None)
    companies = Company.objects.all()

    if form.is_valid():
        keyword = form.cleaned_data.get("keyword")
        location = form.cleaned_data.get("location")
        industry = form.cleaned_data.get("industry")
        company_size = form.cleaned_data.get("company_size")

        if keyword:
            companies = companies.filter(
                Q(name__icontains=keyword) | Q(industry__icontains=keyword)
            )
        if location:
            companies = companies.filter(location__icontains=location)
        if industry:
            companies = companies.filter(industry__icontains=industry)
        if company_size:
            companies = companies.filter(company_size=company_size)

    return render(request, "dashboard/company_search.html", {
        "form": form,
        "companies": companies,
    })
