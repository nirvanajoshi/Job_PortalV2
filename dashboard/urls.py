from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("search/jobs/", views.job_search, name="job_search"),
    path("search/companies/", views.company_search, name="company_search"),
]
