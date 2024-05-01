from django.shortcuts import render
from .models import Polynomial
from django.http import JsonResponse

def base(request):
    return render(request, 'generators/home.html')

def msr(request):
    return render(request, 'generators/msr.html')

def srwf(request):
    # Получаем список степеней
    degrees = Polynomial.objects.values_list('degree', flat=True).distinct()

    return render(request, 'generators/srwf.html', {'degrees': degrees})

def get_polynomials(request):
    selected_degree = request.GET.get('degree')
    polynomials = Polynomial.objects.filter(degree=selected_degree).values('id', 'first_number', 'second_number', 'letter')
    return JsonResponse(list(polynomials), safe=False)

