from django.urls import path
from .views import deleteNotification, showNotifications

urlpatterns = [
    path('', showNotifications, name='show_notifications'),
    path('<notif_id>/delete', deleteNotification, name='delete_notification'),
]
