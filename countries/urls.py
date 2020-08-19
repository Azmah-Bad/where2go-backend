from . import views
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("country/<departure_country>/", views.getRelationships)
]