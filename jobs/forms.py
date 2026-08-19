from django import forms
from django.utils.text import slugify
from .models import Job


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = [
            "title", "description", "requirements", "responsibilities",
            "location", "job_type", "work_mode", "experience_level",
            "salary_min", "salary_max", "application_deadline",
            "skills_required", "vacancies", "is_featured",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 5}
            ),
            "requirements": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "responsibilities": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "job_type": forms.Select(attrs={"class": "form-control"}),
            "work_mode": forms.Select(attrs={"class": "form-control"}),
            "experience_level": forms.Select(attrs={"class": "form-control"}),
            "salary_min": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Min salary"}
            ),
            "salary_max": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Max salary"}
            ),
            "application_deadline": forms.DateInput(
                attrs={"class": "form-control", "type": "date"}
            ),
            "skills_required": forms.Textarea(
                attrs={"class": "form-control", "rows": 2,
                       "placeholder": "Comma-separated: Python, Django, REST API"}
            ),
            "vacancies": forms.NumberInput(
                attrs={"class": "form-control", "min": 1}
            ),
            "is_featured": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        salary_min = cleaned_data.get("salary_min")
        salary_max = cleaned_data.get("salary_max")
        if salary_min and salary_max and salary_min > salary_max:
            raise forms.ValidationError("Minimum salary cannot exceed maximum salary.")
        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.title)
        if self.user and not instance.company_id:
            instance.company = self.user.company
        if commit:
            instance.save()
        return instance


class JobStatusForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
        }
