from django import forms
from .models import JobSeekerProfile


class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = [
            "headline", "bio", "location", "website",
            "linkedin_url", "github_url", "skills",
            "experience_years", "education", "resume",
        ]
        widgets = {
            "headline": forms.TextInput(
                attrs={"class": "form-control",
                       "placeholder": "e.g. Senior Python Developer"}
            ),
            "bio": forms.Textarea(
                attrs={"class": "form-control", "rows": 4,
                       "placeholder": "Tell employers about yourself..."}
            ),
            "location": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "City, Country"}
            ),
            "website": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "https://yoursite.com"}
            ),
            "linkedin_url": forms.URLInput(
                attrs={"class": "form-control",
                       "placeholder": "https://linkedin.com/in/yourprofile"}
            ),
            "github_url": forms.URLInput(
                attrs={"class": "form-control",
                       "placeholder": "https://github.com/yourusername"}
            ),
            "skills": forms.Textarea(
                attrs={"class": "form-control", "rows": 2,
                       "placeholder": "Comma-separated: Python, Django, REST API"}
            ),
            "experience_years": forms.NumberInput(
                attrs={"class": "form-control", "min": 0}
            ),
            "education": forms.Textarea(
                attrs={"class": "form-control", "rows": 3,
                       "placeholder": "Your education history..."}
            ),
            "resume": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and not instance.user_id:
            instance.user = self.user
        if commit:
            instance.save()
        return instance
