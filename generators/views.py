from django.shortcuts import render
from .models import Polynomial
from django.http import JsonResponse
import numpy as np
import json

def base(request):
    return render(request, 'generators/home.html')

def msr(request):
    return render(request, 'generators/msr.html')

def srwf(request):
    # Получаем список степеней
    degrees = Polynomial.objects.values_list('degree', flat=True).distinct()

    return render(request, 'generators/srwf.html', {'degrees': degrees})
    # decimal_number = int(str(polynomial.second_number, 8))
    # binary_number = bin(decimal_number)[2:]
    # second_digit_binary = [int(bit) for bit in binary_number]

def get_polynomials(request):
    selected_degree = request.GET.get('degree')
    polynomials = Polynomial.objects.filter(degree=selected_degree).values('id', 'first_number', 'second_number', 'letter')
    return JsonResponse(list(polynomials), safe=False)

def handle_matrix_operations(request):
    polynomial_id = request.GET.get('polynomial_id')
    polynomial = Polynomial.objects.get(pk=polynomial_id)
    decimal_number = int(str(polynomial.second_number), 8)
    binary_number = bin(decimal_number)[2:]
    second_digit_binary = [int(bit) for bit in binary_number][1:]
    matrix = [[int(digit) for digit in second_digit_binary]]
    for i in range(polynomial.degree - 1):
        row = [0] * polynomial.degree
        row[i] = 1
        matrix.append(row)

    lst = [0] * polynomial.degree
    lst[-1] = 1
    lim = lst
    matrices = []
    matrices.append(lst)
    while True:
        result_array = []
        for row in matrix:
            result = sum([x * y for x, y in zip(row, lst)]) % 2
            result_array.append(result)


        lst = result_array
        if result_array == lim:
            break;
        matrices.append(result_array)
    return JsonResponse({'matrix': matrix, 'result_array': matrices})
