from django import forms
from .models import Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["job", "cover_letter", "resume"]
        widgets = {
            "cover_letter": forms.Textarea(
                attrs={"class": "form-control", "rows": 6,
                       "placeholder": "Write a tailored cover letter..."}
            ),
            "resume": forms.ClearableFileInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user and not instance.job_seeker_id:
            instance.job_seeker = self.user.profile.jobseekerprofile
        if commit:
            instance.save()
        return instance


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["status"]
        widgets = {
            "status": forms.Select(attrs={"class": "form-control"}),
        }
