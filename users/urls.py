from django.contrib import admin
from django.urls import path, include
from users.views import register, profile, custom_register 

urlpatterns = [
    path('register/', register, name = 'register'),
    #path('custom_register/', custom_register, name = 'custom_register'),
    path('profile/', profile, name = 'profile'),
]
