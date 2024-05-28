from django.core.exceptions import ValidationError
from django.shortcuts import render
from .models import Polynomial
from django.http import JsonResponse
from .SrwfCalculator.SrwfCalculator import SrwfCalculator
from .MsrCalculator.MsrCalculator import MsrCalculator
from .SrwfCalculator.PRNG import BinaryToAverageModel
from .utils import validation, get_polynomials

def base(request):
    return render(request, 'generators/home.html')

def msr(request):
    degrees = Polynomial.objects.values_list('degree', flat=True).distinct()
    return render(request, 'generators/msr.html',  {'degrees': degrees})

def srwf(request):
    degrees = Polynomial.objects.values_list('degree', flat=True).distinct()
    return render(request, 'generators/srwf.html', {'degrees': degrees})

def get_polynomials_view(request):
    return get_polynomials(request)

def handle_matrix_operations_view(request):
    polynomial_id = request.GET.get('polynomial_id')
    polynomial = Polynomial.objects.get(pk=polynomial_id)
    selected_number = int(request.GET.get('select'))
    
    cal = SrwfCalculator()
    result = cal.calculate_srwf(polynomial, selected_number)
    
    btam = BinaryToAverageModel()
    btam.load_model()
    string_sequence = ''.join(map(str, result['sequence']))
    binary_representations_to_predict = [string_sequence]
    print(binary_representations_to_predict)   
    predicted_average_numbers = btam.predict(binary_representations_to_predict)
    result["rlst"] = predicted_average_numbers.tolist()
    
    return JsonResponse({'result': result})

def handle_matrix_operations_msr_view(request):
    polynomial_idFirst = request.GET.get('polynomial_idFirst')
    polynomialFirst = Polynomial.objects.get(pk=polynomial_idFirst)
    polynomial_idSecond = request.GET.get('polynomial_idSecond')
    polynomialSecond = Polynomial.objects.get(pk=polynomial_idSecond)
    degreeFirst = int(request.GET.get('degreeFirst'))
    degreeSecond = int(request.GET.get('degreeSecond'))
    i = int(request.GET.get('i'))
    j = int(request.GET.get('j'))
    r = int(request.GET.get('r'))
    try:
        validate_result, error_message = validation(degreeFirst, polynomialFirst.first_number, degreeSecond,
                                                    polynomialSecond.first_number)
        if validate_result:
            raise ValidationError(error_message)

        cal = MsrCalculator()
        listResult = cal.calculate_msr(polynomialFirst, polynomialSecond, i, j, r)
        return JsonResponse({'listResult': listResult})
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

