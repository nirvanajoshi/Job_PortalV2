from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "recipient",
        "verb",
        "is_read",
        "created_at",
    )
    list_filter = (
        "is_read",
        "created_at",
    )
    search_fields = (
        "recipient__username",
        "recipient__email",
        "verb",
        "description",
    )
    readonly_fields = ("created_at",)

    fieldsets = (
        (
            "Notification Information",
            {
                "fields": (
                    "recipient",
                    "verb",
                    "description",
                    "target_url",
                    "is_read",
                )
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at",),
                "classes": ("collapse",),
            },
        ),
    )

    ordering = ("-created_at",)
    date_hierarchy = "created_at"