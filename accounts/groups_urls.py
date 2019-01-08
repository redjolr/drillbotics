from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.allgroups, name='allgroups'),
    path('<int:id>/', views.group, name='group'),
    path('<int:id>/delete/', views.delete_group, name='delete_group'),
    path('add/', views.addgroup, name='addgroup'),
    path('permissions/get/', views.get_permissions, name='get_permissions'),


]
