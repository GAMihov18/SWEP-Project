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

import front_end.views as fe
import api.views as api

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.root),
    path("api/reports", api.reports),
    path("", fe.home, name="home-page"),
    path("login/", fe.login, name="login-page"),
    path("register/", fe.register, name="register-page"),
    path("map/", fe.map)
]
