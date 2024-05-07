from django.shortcuts import render
from .models import Polynomial
from django.http import JsonResponse
from .SrwfCalculator.SrwfCalculator import SrwfCalculator

def base(request):
    return render(request, 'generators/home.html')

def msr(request):
    return render(request, 'generators/msr.html')

def srwf(request):
    degrees = Polynomial.objects.values_list('degree', flat=True).distinct()
    return render(request, 'generators/srwf.html', {'degrees': degrees})

def get_polynomials_view(request):
    return SrwfCalculator.get_polynomials(request)

def handle_matrix_operations_view(request):
    polynomial_id = request.GET.get('polynomial_id')
    selected_number = int(request.GET.get('select'))
    cal = SrwfCalculator()
    result = cal.calculate_srwf(polynomial_id, selected_number)
    return JsonResponse({'result': result})
