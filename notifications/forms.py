from django import forms
from .models import Notification


class NotificationFilterForm(forms.Form):
    notification_type = forms.ChoiceField(
        required=False,
        choices=[("", "All Types")] + list(Notification.NOTIFICATION_TYPE_CHOICES),
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    is_read = forms.ChoiceField(
        required=False,
        choices=[
            ("", "All"),
            ("false", "Unread"),
            ("true", "Read"),
        ],
        widget=forms.Select(attrs={"class": "form-control"}),
    )


class NotificationBulkActionForm(forms.Form):
    ACTION_CHOICES = (
        ("", "Select action"),
        ("mark_read", "Mark as read"),
        ("mark_unread", "Mark as unread"),
        ("delete", "Delete"),
    )

    notification_ids = forms.CharField(
        widget=forms.HiddenInput(),
    )
    action = forms.ChoiceField(
        choices=ACTION_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    def clean_notification_ids(self):
        raw = self.cleaned_data["notification_ids"]
        if not raw:
            raise forms.ValidationError("No notifications selected.")
        return [int(nid) for nid in raw.split(",") if nid.strip().isdigit()]
