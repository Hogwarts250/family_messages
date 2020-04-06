from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Message

def home(request):
    users = User.objects.values()
    usernames = []

    for user in users:
        username = user["username"]
        if username != "admin":
            usernames.append(username)

    context = {"usernames": usernames}

    return render(request, "family_messages/home.html", context)

def message(request):
    messages = Message.objects.order_by()