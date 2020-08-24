from rest_framework import routers

from . import views
from django.contrib import admin
from django.urls import include, path

from .views import RestView

router = routers.DefaultRouter()
router.register(r'relationships', RestView)

urlpatterns = [
    path('', include(router.get_urls())),
    path("country/<departure_country>/", views.getRelationships)
]
