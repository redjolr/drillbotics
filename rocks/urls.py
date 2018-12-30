from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.allrocks, name='rocks'),
    path('<int:id>/', views.rock, name='rock'),
    path('add/', views.addrock, name='addrock'),
    path('update/<int:id>', views.update_rock, name='update_rock'),
    path('getmaterials', views.get_materials, name='get_materials'),
    path('materials/add', views.add_materials, name='add_materials')


]
