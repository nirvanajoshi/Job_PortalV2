from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from .models import Company
from .forms import CompanyForm
from jobs.models import Job


def company_list(request):
    """List all companies."""
    companies = Company.objects.all()
    industry_filter = request.GET.get("industry", "")
    if industry_filter:
        companies = companies.filter(industry__icontains=industry_filter)

    return render(request, "companies/company_list.html", {
        "companies": companies,
        "current_industry": industry_filter,
    })


def company_detail(request, slug):
    """View a specific company's details and its published jobs."""
    company = get_object_or_404(Company, slug=slug)
    jobs = Job.objects.filter(company=company, status="published")

    return render(request, "companies/company_detail.html", {
        "company": company,
        "jobs": jobs,
    })


@login_required
def company_create(request):
    """Create a new company (employer only)."""
    if request.user.profile.role != "employer":
        messages.error(request, "Only employers can create a company.")
        return redirect("dashboard:dashboard")

    if Company.objects.filter(owner=request.user).exists():
        messages.warning(request, "You already have a company. You can edit it instead.")
        return redirect("companies:company_edit", slug=request.user.company.slug)

    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            company = form.save()
            messages.success(request, f"{company.name} has been created!")
            return redirect("companies:company_detail", slug=company.slug)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CompanyForm(user=request.user)

    return render(request, "companies/company_form.html", {"form": form, "action": "Create"})


@login_required
def company_edit(request, slug):
    """Edit company details (owner only)."""
    company = get_object_or_404(Company, slug=slug)

    if company.owner != request.user:
        raise PermissionDenied("You do not have permission to edit this company.")

    if request.method == "POST":
        form = CompanyForm(request.POST, request.FILES, instance=company, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Company details have been updated!")
            return redirect("companies:company_detail", slug=company.slug)
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CompanyForm(instance=company, user=request.user)

    return render(request, "companies/company_form.html", {"form": form, "company": company, "action": "Edit"})


@login_required
def company_delete(request, slug):
    """Delete a company (owner only)."""
    company = get_object_or_404(Company, slug=slug)

    if company.owner != request.user:
        raise PermissionDenied("You do not have permission to delete this company.")

    if request.method == "POST":
        company_name = company.name
        company.delete()
        messages.info(request, f"{company_name} has been deleted.")
        return redirect("dashboard:dashboard")

    return render(request, "companies/company_confirm_delete.html", {"company": company})
