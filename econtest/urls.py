"""
URL configuration for econtest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from app.views import register_view
from app.views import login_view
from app.views import dashboard_view
from app.views import standings_view
from app.views import submissions_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', register_view, name="register"),
    path('login/', login_view, name="login"),
    path('', login_view, name="login"),
    path('dashboard/', dashboard_view, name="dashboard"),
    path('standings/', standings_view, name="standings"),
    path('submissions/', submissions_view, name="submissions"),
]