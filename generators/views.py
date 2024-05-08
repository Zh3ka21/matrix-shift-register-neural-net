from django.shortcuts import render
from .models import Polynomial
from django.http import JsonResponse
from .SrwfCalculator.SrwfCalculator import SrwfCalculator
from .MsrCalculator.MsrCalculator import MsrCalculator

def base(request):
    return render(request, 'generators/home.html')

def msr(request):
    degrees = Polynomial.objects.values_list('degree', flat=True).distinct()
    return render(request, 'generators/msr.html',  {'degrees': degrees})

def srwf(request):
    degrees = Polynomial.objects.values_list('degree', flat=True).distinct()
    return render(request, 'generators/srwf.html', {'degrees': degrees})

def get_polynomials_view(request):
    return SrwfCalculator.get_polynomials(request)

def handle_matrix_operations_view(request):
    polynomial_id = request.GET.get('polynomial_id')
    polynomial = Polynomial.objects.get(pk=polynomial_id)
    selected_number = int(request.GET.get('select'))
    cal = SrwfCalculator()
    result = cal.calculate_srwf(polynomial, selected_number)
    return JsonResponse({'result': result})

def handle_matrix_operations_msr_view(request):
    polynomial_idFirst = request.GET.get('polynomial_idFirst')
    polynomialFirst = Polynomial.objects.get(pk=polynomial_idFirst)
    polynomial_idSecond = request.GET.get('polynomial_idSecond')
    polynomialSecond = Polynomial.objects.get(pk=polynomial_idSecond)
    cal = MsrCalculator()
    listResult = cal.calculate_msr(polynomialFirst, polynomialSecond)
    return JsonResponse({'listResult': listResult})