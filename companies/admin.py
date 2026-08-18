from django.contrib import admin
from .models import Company


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "industry",
        "location",
        "company_size",
        "is_verified",
        "created_at",
    )
    list_filter = (
        "industry",
        "company_size",
        "is_verified",
        "created_at",
    )
    search_fields = (
        "name",
        "owner__username",
        "owner__email",
        "industry",
        "location",
    )
    readonly_fields = ("created_at", "updated_at")
    
    fieldsets = (
        ("Company Information", {
            "fields": (
                "name",
                "owner",
                "description",
                "industry",
                "company_size",
            )
        }),
        ("Contact Information", {
            "fields": (
                "website",
                "location",
            )
        }),
        ("Verification", {
            "fields": (
                "is_verified",
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