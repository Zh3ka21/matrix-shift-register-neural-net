from django.urls import path
from . import views
from .views import download_excel, download_word, display_excel, display_word

urlpatterns = [
    path('', views.base, name='base'),
    path('msr/', views.msr, name='msr'),
    path('srwf/', views.srwf, name='srwf'),
    path('get_polynomials_view/', views.get_polynomials_view, name='get_polynomials_view'),
    path('handle_matrix_operations_view/', views.handle_matrix_operations_view, name='handle_matrix_operations_view'),
    path('handle_matrix_operations_msr_view/', views.handle_matrix_operations_msr_view, name='handle_matrix_operations_msr_view'),
    path('download-excel/', download_excel, name='download_excel'),
    path('download-word/', download_word, name='download_word'),
    path('display-excel/', display_excel, name='display_excel'),
    path('display-word/', display_word, name='display_word'),
]
