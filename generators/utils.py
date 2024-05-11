from .models import Polynomial
from django.http import JsonResponse
def power(n):
    return 2 ** n - 1


def find_gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def validation(degreeA, first_digitA, degreeB, first_digitB):
    denominator = find_gcd(power(degreeA), power(degreeB))
    if denominator != 1:
        print(" 1 " + str(denominator))
        return True, "Degrees error"

    numerator = power(degreeA)
    denominator = find_gcd(numerator, first_digitA)
    result = numerator / denominator
    if result != numerator:
        print(" 2 " + str(result))
        return True, "Degrees and polynomial not competible, A"

    numerator = power(degreeB)
    denominator = find_gcd(numerator, first_digitB)
    result = numerator / denominator
    if result != numerator:
        print(" 3 " + str(result))
        return True, "Degrees and polynomial not competible, B"

    return False, ""


def get_polynomials(request):
    selected_degree = request.GET.get('degree')
    polynomials = Polynomial.objects.filter(degree=selected_degree).values('id', 'first_number', 'second_number',
                                                    'letter')
    return JsonResponse(list(polynomials), safe=False)
