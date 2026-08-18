from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "title",
        "is_read",
        "created_at",
    )
    list_filter = (
        "is_read",
        "created_at",
    )
    search_fields = (
        "user__username",
        "user__email",
        "title",
        "description",
    )
    readonly_fields = ("created_at",)

    fieldsets = (
        (
            "Notification Information",
            {
                "fields": (
                    "user",
                    "title",
                    "message",
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