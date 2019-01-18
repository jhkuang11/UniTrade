from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import ComposeForm
from django.utils import timezone
from onlinestore.models import Category

"""
Views for the message app.

:Date: 2018-11-13
:Authors:
    - Jianhong Kuang
    - Xinhuan Qiu
"""

def home(request):
    """The view for user dashboard - message section which contains inbox,
    outbox and compose tabs.

    :param request:
    :return: rendered message home template with received, sent messages,
    the compose message form and categories for navbar dropdown list.
    """
    if request.method == "POST":
        form = ComposeForm(request.POST)
        if form.is_valid():
            user = request.user
            post = form.save(commit=False)
            post.sender = user
            post.timestamp = timezone.now()
            post.save()
            return redirect('/message/')
    else:
        form = ComposeForm()

    received_msg = Messages.objects.filter(receiver=request.user).order_by('-timestamp')
    sent_msg = Messages.objects.filter(sender=request.user).order_by('-timestamp')

    categories = Category.objects.all()
    return render(request, 'message/home.html', {'received_msg': received_msg, 'sent_msg': sent_msg, 'form': form, 'categories': categories})

def inbox(request):
    msg_list = Messages.objects.filter(receiver=request.user)
    categories = Category.objects.all()
    return render(request, 'message/inbox.html', {'message_list': msg_list, 'categories': categories})

def outbox(request):
    msg_list = Messages.objects.filter(sender=request.user)
    categories = Category.objects.all()
    return render(request, 'message/outbox.html', {'message_list': msg_list, 'categories': categories})

def compose(request):
    if request.method == "POST":
        form = ComposeForm(request.POST)
        if form.is_valid():
            user = request.user
            post = form.save(commit=False)
            post.sender = user
            post.timestamp = timezone.now()
            post.save()
            return redirect('/message/')
    else:
        form = ComposeForm()

    categories = Category.objects.all()
    return render(request, 'message/compose.html', {'form': form, 'categories': categories})