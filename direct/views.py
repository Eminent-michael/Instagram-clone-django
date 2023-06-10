from django.shortcuts import render, redirect
from .models import Message

from django.template import loader
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
@login_required
def inbox(request):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct = None
    directs = None

    # Opening the messages
    if messages:
        message = messages[0]
        active_direct = message["user"].username
        directs = Message.objects.filter(user=user, recipient=message["user"])
        directs.update(is_read=True)

        for message in messages:
            if message["user"].username == active_direct:
                message["unread"] = 0

    context = {
        "directs": directs,
        "active_direct": active_direct,
        "messages": messages,
    }

    template = loader.get_template("direct/direct.html")
    return HttpResponse(template.render(context, request))


@login_required
def directs(request, username):
    user = request.user
    messages = Message.get_messages(user=user)
    active_direct = username
    directs = Message.objects.filter(user=user, recipient__username=username)
    directs.update(is_read=True)

    for message in messages:
        if message["user"].username == username:
            message["unread"] = 0

    context = {
        "messages": messages,
        "directs": directs,
        "active_direct": active_direct,
    }

    template = loader.get_template("direct/direct.html")
    return HttpResponse(template.render(context, request))
                        
                        
@login_required # type: ignore
def sendDirect(request):
    from_user = request.user
    to_user_username = request.POST.get("to_user")
    body = request.POST.get("body")

    if request.method == "POST":
        to_user = User.objects.get(username=to_user_username)
        Message.send_message(from_user, to_user, body)
        return redirect("inbox")
    else:
        return HttpResponseBadRequest


@login_required
def userSearch(request):
    query = request.GET.get("q")
    context = {}

    if query:
        users = User.objects.filter(Q(username__icontains=query))

        # Paginator
        paginator = Paginator(users, 6)
        page_number = request.GET.get("page")
        users_paginator = paginator.get_page(page_number)

        context = {"users": users_paginator}

    template = loader.get_template("direct/search_user.html")
    return HttpResponse(template.render(context, request))


def newConversation(request, username):
    from_user = request.user
    body = "Says Hello!"

    try:
        to_user = User.objects.get(username=username)
    except Exception as e:
        return redirect("usersearch")
    if from_user != to_user:
        Message.send_message(from_user, to_user, body)

    return redirect("inbox")


def countDirects(request):
    directs_count = 0
    if request.user.is_authenticated:
        directs_count = Message.objects.filter(user=request.user, is_read=False).count()

    return {"direct_counts": directs_count}
