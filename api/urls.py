from django.contrib import admin
from django.urls import path, include
from api import views


urlpatterns = [
    path('addexperiment/<str:checksum>/', views.addexperiment, name='addexperiment'),
    path('upload_chunk/<str:checksum>/', views.upload_chunk, name='upload_chunk'),
    path('getsensors/', views.getsensors, name='getsensors'),
    path('getrocks/', views.getrocks, name='getrocks'),
    path('getrocksandsensors/', views.getrocksandsensors, name='getrocksandsensors'),
]
