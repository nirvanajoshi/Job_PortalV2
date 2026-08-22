from django.urls import path
from . import views

app_name = "profiles"

urlpatterns = [
    path("jobseeker/<str:username>/", views.jobseeker_profile_view, name="jobseeker_profile"),
    path("jobseeker/edit/", views.jobseeker_profile_edit, name="jobseeker_profile_edit"),
    path("jobseeker/create/", views.jobseeker_profile_create, name="jobseeker_profile_create"),
]
