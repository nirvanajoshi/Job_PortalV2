from django.urls import path
from . import views

app_name = "companies"

urlpatterns = [
    path("", views.company_list, name="company_list"),
    path("create/", views.company_create, name="company_create"),
    path("<slug:slug>/", views.company_detail, name="company_detail"),
    path("<slug:slug>/edit/", views.company_edit, name="company_edit"),
    path("<slug:slug>/delete/", views.company_delete, name="company_delete"),
]
