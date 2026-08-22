from django.urls import path
from . import views

app_name = "applications"

urlpatterns = [
    path("", views.application_list, name="application_list"),
    path("<int:pk>/", views.application_detail, name="application_detail"),
    path("job/<int:job_pk>/apply/", views.apply_job, name="apply_job"),
    path("<int:pk>/withdraw/", views.withdraw_application, name="withdraw_application"),
    path("employer/", views.employer_applications, name="employer_applications"),
    path("<int:pk>/update-status/", views.update_application_status, name="update_application_status"),
]
