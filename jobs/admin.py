from django.contrib import admin
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "job_type",
        "location",
        "is_active",
        "posted_at",
    )
    list_filter = (
        "job_type",
        "is_active",
        "posted_at",
    )
    search_fields = (
        "title",
        "description",
        "company__name",
        "location",
    )
    readonly_fields = ("posted_at", "updated_at")
    
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
                "is_active",
            )
        }),
        ("Timestamps", {
            "fields": (
                "posted_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )
    
    ordering = ("-posted_at",)
    date_hierarchy = "posted_at"