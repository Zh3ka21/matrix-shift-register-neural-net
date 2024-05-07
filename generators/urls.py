from django.urls import path
from . import views

urlpatterns = [
    path('', views.base, name='base'),
    path('msr/', views.msr, name='msr'),
    path('srwf/', views.srwf, name='srwf'),
    path('get_polynomials_view/', views.get_polynomials_view, name='get_polynomials_view'),
    path('handle_matrix_operations_view/', views.handle_matrix_operations_view, name='handle_matrix_operations_view')
]
