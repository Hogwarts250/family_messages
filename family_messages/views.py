from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import Message
from .forms import MessageForm

def home(request):
    users = User.objects.all()
    usernames = [username for username in users.values_list("username", flat=True) if username != "admin"]

    context = {"usernames": usernames}

    return render(request, "family_messages/home.html", context)

@login_required
def view_message(request, username):
    users = User.objects.all()
    usernames = [username for username in users.values_list("username", flat=True) if username != "admin"]

    user = users.get(username__exact=username)
    message = Message.objects.all().get(owner__exact=user)

    context = {"username": username, "usernames": usernames, "message": message}

    return render(request, "family_messages/message.html", context)

@login_required
def edit_message(request, username):
    users = User.objects.all()
    usernames = [username for username in users.values_list("username", flat=True) if username != "admin"]

    user = users.get(username__exact=username)
    message = Message.objects.all().get(owner__exact=user)

    if request.method != "POST":
        form = MessageForm(instance=message)

    else:
        form = MessageForm(instance=message, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("family_messages:home"))

    context = {"username": username, "usernames": usernames, "message": message, "form": form}
    
    return render(request, "family_messages/edit_message.html", context)