"""where2go URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include, path
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers

from rest_framework.authtoken import views

from countries.views import test, RestView
from where2go.views import Logout

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('countries.urls')),
    path('api-auth/', include('rest_framework.urls')),
    url(r'^token/', views.obtain_auth_token),
    url('logout/', Logout.as_view()),
    path('test/',test)

]


