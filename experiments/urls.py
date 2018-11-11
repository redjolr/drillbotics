from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.allexperiments, name='experiments'),
    path('<int:id>', views.experiment_data, name='experiment_data'),
    path('download/<int:experiment_id>', views.download_dataset, name='download_dataset'),
    # path('<int:id>/', views.sensor, name='sensor'),
    # path('add/', views.addsensor, name='addsensor')
]
