from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

def login_view(request):    
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("family_messages:home"))

    users = User.objects.all()
    usernames = [username for username in users.values_list("username", flat=True) if username != "admin"]
    
    form = AuthenticationForm()

    context = {"usernames": usernames, "form": form}

    return render(request, "users/login.html", context)

def logout_view(request):
    logout(request)
    
    return HttpResponseRedirect(reverse("family_messages:home"))