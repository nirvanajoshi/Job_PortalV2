from django import forms
from jobs.models import Job
from companies.models import Company
from applications.models import Application


class JobSearchForm(forms.Form):
    keyword = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search by title, skill, or keyword..."
        }),
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Location"
        }),
    )
    job_type = forms.ChoiceField(
        required=False,
        choices=[("", "All Types")] + list(Job.JOB_TYPE_CHOICES),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    work_mode = forms.ChoiceField(
        required=False,
        choices=[("", "All Modes")] + list(Job.WORK_MODE_CHOICES),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    experience_level = forms.ChoiceField(
        required=False,
        choices=[("", "All Levels")] + list(Job.EXPERIENCE_LEVEL_CHOICES),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    salary_min = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "form-control", "placeholder": "Min salary"
        }),
    )
    salary_max = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            "class": "form-control", "placeholder": "Max salary"
        }),
    )


class CompanySearchForm(forms.Form):
    keyword = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search by name or industry..."
        }),
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Location"
        }),
    )
    industry = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Industry"
        }),
    )
    company_size = forms.ChoiceField(
        required=False,
        choices=[("", "All Sizes")] + list(Company.COMPANY_SIZE_CHOICES),
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class ApplicationFilterForm(forms.Form):
    status = forms.ChoiceField(
        required=False,
        choices=[("", "All Statuses")] + list(Application.STATUS_CHOICES),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
