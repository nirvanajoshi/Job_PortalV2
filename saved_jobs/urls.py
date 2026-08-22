from django.urls import path
from . import views

app_name = "saved_jobs"

urlpatterns = [
    path("", views.saved_job_list, name="saved_job_list"),
    path("job/<int:job_pk>/save/", views.save_job, name="save_job"),
    path("<int:pk>/unsave/", views.unsave_job, name="unsave_job"),
    path("bulk-unsave/", views.bulk_unsave, name="bulk_unsave"),
]
