from django.urls import path
from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.job_list, name="job_list"),
    path("<int:pk>/", views.job_detail, name="job_detail"),
    path("create/", views.job_create, name="job_create"),
    path("<int:pk>/edit/", views.job_update, name="job_update"),
    path("<int:pk>/delete/", views.job_delete, name="job_delete"),
    path("<int:pk>/update-status/", views.update_job_status, name="update_job_status"),
]
