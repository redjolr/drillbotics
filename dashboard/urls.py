from django.contrib import admin
from django.urls import path, include
import dashboard.views
urlpatterns = [
    path('', dashboard.views.home , name='dashboard')
]
