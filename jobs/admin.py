from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "job_type",
        "location",
        "status",
        "created_at",
    )
    list_filter = (
        "job_type",
        "status",
        "created_at",
    )
    search_fields = (
        "title",
        "description",
        "company__name",
        "location",
    )
    readonly_fields = ("created_at", "updated_at")
    
    fieldsets = (
        ("Job Details", {
            "fields": (
                "company",
                "title",
                "description",
                "job_type",
                "location",
                "salary_range",
            )
        }),
        ("Status", {
            "fields": (
                "status",
            )
        }),
        ("Timestamps", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )
    
    ordering = ("-created_at",)
    date_hierarchy = "created_at"