"""
URL configuration for afmers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from front_end import views

import front_end.views as fe
import api.views as api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.root),
    path("api/auth/login", api.login),
    path("api/auth/register", api.register),
    path("api/reports", api.reports),
    path("", views.Home, name="home-page"),
    path("login/", LoginView.as_view(template_name="Login.html"), name="login-page"),
    path("register/", views.register, name="register-page"),
]
