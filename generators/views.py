from django.core.exceptions import ValidationError
from django.shortcuts import render
from .models import Polynomial
from django.http import JsonResponse
from .SrwfCalculator.SrwfCalculator import SrwfCalculator
from .MsrCalculator.MsrCalculator import MsrCalculator
from .SrwfCalculator.PRNG import RandomNumberModel
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
    rnm = RandomNumberModel()
    rnm.load_model()  # Load the model
    r_n_lst = rnm.generate_random_numbers(n = 10)
    result["rlst"] = r_n_lst
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

