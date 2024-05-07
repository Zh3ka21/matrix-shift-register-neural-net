from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('msr/', views.msr, name='msr'),
    path('srwf/', views.srwf, name='srwf'),
    path('get_polynomials/', views.get_polynomials, name='get_polynomials'),
    path('handle_matrix_operations/', views.handle_matrix_operations, name='handle_matrix_operations')
]
