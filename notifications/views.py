from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Notification
from .forms import NotificationFilterForm, NotificationBulkActionForm


@login_required
def notification_list(request):
    """List all notifications for the logged-in user with filtering."""
    notification_list_qs = Notification.objects.filter(user=request.user)
    form = NotificationFilterForm(request.GET or None)
    unread_count = notification_list_qs.filter(is_read=False).count()

    if form.is_valid():
        notification_type = form.cleaned_data.get("notification_type")
        is_read = form.cleaned_data.get("is_read")

        if notification_type:
            notification_list_qs = notification_list_qs.filter(
                notification_type=notification_type
            )
        if is_read == "true":
            notification_list_qs = notification_list_qs.filter(is_read=True)
        elif is_read == "false":
            notification_list_qs = notification_list_qs.filter(is_read=False)

    bulk_form = NotificationBulkActionForm()

    return render(request, "notifications/notification_list.html", {
        "notifications": notification_list_qs,
        "form": form,
        "bulk_form": bulk_form,
        "unread_count": unread_count,
    })


@login_required
def notification_detail(request, pk):
    """View a specific notification and mark it as read."""
    notification = get_object_or_404(
        Notification, pk=pk, user=request.user
    )
    if not notification.is_read:
        notification.is_read = True
        notification.save(update_fields=["is_read"])

    return render(request, "notifications/notification_detail.html", {
        "notification": notification,
    })


@login_required
@require_POST
def mark_notification_read(request, pk):
    """Mark a single notification as read."""
    notification = get_object_or_404(
        Notification, pk=pk, user=request.user
    )
    notification.is_read = True
    notification.save(update_fields=["is_read"])

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"status": "ok", "id": notification.pk})

    return redirect("notifications:notification_list")


@login_required
@require_POST
def mark_all_read(request):
    """Mark all notifications as read."""
    updated = Notification.objects.filter(
        user=request.user, is_read=False
    ).update(is_read=True)

    messages.success(request, f"{updated} notification(s) marked as read.")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"status": "ok", "count": updated})

    return redirect("notifications:notification_list")


@login_required
@require_POST
def bulk_action(request):
    """Perform bulk actions on selected notifications."""
    form = NotificationBulkActionForm(request.POST)
    if form.is_valid():
        ids = form.cleaned_data["notification_ids"]
        action = form.cleaned_data["action"]
        notifications = Notification.objects.filter(
            pk__in=ids, user=request.user
        )

        if action == "mark_read":
            count = notifications.update(is_read=True)
            messages.success(request, f"{count} notification(s) marked as read.")
        elif action == "mark_unread":
            count = notifications.update(is_read=False)
            messages.success(request, f"{count} notification(s) marked as unread.")
        elif action == "delete":
            count = notifications[0:0].count()  # count before delete
            notifications.delete()
            messages.success(request, f"{len(ids)} notification(s) deleted.")

    return redirect("notifications:notification_list")


@login_required
@require_POST
def delete_notification(request, pk):
    """Delete a single notification."""
    notification = get_object_or_404(
        Notification, pk=pk, user=request.user
    )
    notification.delete()
    messages.info(request, "Notification deleted.")

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({"status": "ok", "id": pk})

    return redirect("notifications:notification_list")
