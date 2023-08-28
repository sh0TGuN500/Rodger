from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'weather'

urlpatterns = [
    path('', views.home),
]
