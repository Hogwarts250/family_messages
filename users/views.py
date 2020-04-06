from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import views as auth_views, logout

class LoginView(auth_views.LoginView):
    template_name = "users/login.html"

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("family_messages:home"))