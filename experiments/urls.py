from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.allexperiments, name='experiments'),
    path('<int:id>/<int:sensor_id>', views.experiment_data, name='experiment_data')
    # path('<int:id>/', views.sensor, name='sensor'),
    # path('add/', views.addsensor, name='addsensor')
]
