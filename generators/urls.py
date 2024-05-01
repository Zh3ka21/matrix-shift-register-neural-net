from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('msr/', views.msr, name='msr'),
    path('srwf/', views.srwf, name='srwf'),
]