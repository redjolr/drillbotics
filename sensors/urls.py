from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.allsensors, name='sensors'),
    path('<int:id>/', views.sensor, name='sensor'),
    path('add/', views.addsensor, name='addsensor'),
    path('update/<int:id>', views.update_sensor, name='update_sensor')
]
