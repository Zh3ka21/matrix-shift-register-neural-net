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

def get_polynomials(request):
    selected_degree = request.GET.get('degree')
    polynomials = Polynomial.objects.filter(degree=selected_degree).values('id', 'first_number', 'second_number', 'letter')
    return JsonResponse(list(polynomials), safe=False)

def handle_matrix_operations(request):

    polynomial_id = request.GET.get('polynomial_id')
    polynomial = Polynomial.objects.get(pk=polynomial_id)
    print(polynomial)
    selected_number = int(request.GET.get('select'))
    binary_representation = format(selected_number, f'0{int(polynomial.degree)}b')

    decimal_number = int(str(polynomial.second_number), 8)
    binary_number = bin(decimal_number)[2:]
    second_digit_binary = [int(bit) for bit in binary_number][1:]

    matrix = [[int(digit) for digit in second_digit_binary]]
    for i in range(polynomial.degree - 1):
        row = [0] * polynomial.degree
        row[i] = 1
        matrix.append(row)

    lst = [int(i) for i in binary_representation]
    lim = lst
    matrices = []
    matrices.append(lst)
    sequence = []

    while True:
        sequence.append(lst[-1])
        result_array = []

        for row in matrix:
            result = sum([x * y for x, y in zip(row, lst)]) % 2
            result_array.append(result)

        lst = result_array

        if result_array == lim:
            break
        matrices.append(result_array)

    binary_sequence = [1 if i == 0 else -1 for i in sequence]
    T = pow(2, polynomial.degree) - 1
    hg = len([i for i in sequence if i == 1])
    T_e = T / find_gcd(T, polynomial.first_number)
    T_r = len(sequence)
    return JsonResponse({'matrix': matrix, 'result_array': matrices, 'sequence': sequence, 'binary_sequence': binary_sequence,
                         'hg': hg, 'T_e': T_e, 'T_r': T_r})

def find_gcd(a, b):
    while b:
        a, b = b, a % b
    return a