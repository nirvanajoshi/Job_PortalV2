from django import forms
from .models import SavedJob


class SaveJobForm(forms.ModelForm):
    class Meta:
        model = SavedJob
        fields = ["job"]
        widgets = {
            "job": forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.job_seeker = self.user.profile.jobseekerprofile
        if commit:
            instance.save()
        return instance


class SavedJobBulkActionForm(forms.Form):
    ACTION_CHOICES = (
        ("", "Select action"),
        ("unsave", "Remove selected"),
    )

    saved_job_ids = forms.CharField(widget=forms.HiddenInput())
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def clean_saved_job_ids(self):
        raw = self.cleaned_data["saved_job_ids"]
        if not raw:
            raise forms.ValidationError("No saved jobs selected.")
        return [int(nid) for nid in raw.split(",") if nid.strip().isdigit()]
