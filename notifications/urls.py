from django.urls import path
from . import views

app_name = "notifications"

urlpatterns = [
    path("", views.notification_list, name="notification_list"),
    path("<int:pk>/", views.notification_detail, name="notification_detail"),
    path("<int:pk>/read/", views.mark_notification_read, name="mark_notification_read"),
    path("mark-all-read/", views.mark_all_read, name="mark_all_read"),
    path("bulk-action/", views.bulk_action, name="bulk_action"),
    path("<int:pk>/delete/", views.delete_notification, name="delete_notification"),
]
