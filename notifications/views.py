from django.shortcuts import render, redirect
from .models import Notifications
from django.http import HttpResponse
from django.template import loader

# Create your views here.

def showNotifications(request):
    user = request.user
    notifications = Notifications.objects.filter(user=user).order_by('-date')
    Notifications.objects.filter(user=user, is_seen=False).update(is_seen=True)
    
    template = loader.get_template('notification.html')
    context = {
        'notifications': notifications,
    }
    return HttpResponse(template.render(context, request))

def deleteNotification(request, notif_id):
    user = request.user
    Notifications.objects.filter(user=user, id=notif_id).delete()
    return redirect('show_notifications')

def countNotifications(request):
    count_notifications = 0
    if request.user.is_authenticated:
        count_notifications = Notifications.objects.filter(user=request.user, is_seen=False).count()
    return {'count_notifications': count_notifications}
    