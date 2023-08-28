from django.urls import path, include
from rest_framework import routers

from . import views

app_name = 'home'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('language_switch/<str:user_language>/', views.lang_switcher, name='lang'),
]
