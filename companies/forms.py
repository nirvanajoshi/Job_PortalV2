from django import forms
from django.utils.text import slugify
from .models import Company


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = [
            "name", "description", "logo", "website", "email",
            "phone", "industry", "location", "company_size",
            "founded_year",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(
                attrs={"class": "form-control", "rows": 5}
            ),
            "logo": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "website": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "https://"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "company@example.com"}
            ),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "industry": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g. Technology"}
            ),
            "location": forms.TextInput(attrs={"class": "form-control"}),
            "company_size": forms.Select(attrs={"class": "form-control"}),
            "founded_year": forms.NumberInput(
                attrs={"class": "form-control", "min": 1900}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data.get("name")
        slug = slugify(name)
        qs = Company.objects.filter(slug=slug)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("A company with a similar name already exists.")
        return name

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.slug = slugify(instance.name)
        if self.user and not instance.owner_id:
            instance.owner = self.user
        if commit:
            instance.save()
        return instance
