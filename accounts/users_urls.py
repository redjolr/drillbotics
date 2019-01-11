from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.allusers, name='allusers'),
    path('add/', views.adduser, name='adduser'),
    path('<int:id>/', views.user, name='user'),
    path('get_groups/', views.get_groups, name='get_groups'),
    path('change_password/', views.change_password, name='change_password'),

]
