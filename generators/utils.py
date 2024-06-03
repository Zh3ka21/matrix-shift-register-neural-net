from .models import Polynomial
from django.http import JsonResponse
def power(n):
    return 2 ** n - 1

def lcm(a, b):
    return abs(a * b) // find_gcd(a, b)

def find_gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def validation(degreeA, first_digitA, degreeB, first_digitB):

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


def get_acf(self):
        RCr = []
        k = self.T_r  # Assuming self.T is the length of the sequence
        for tilda in range(k):
            autocorr_sum = 0
            for t in range(k):
                autocorr_sum += self.binary_sequence[t] * self.binary_sequence[(t + tilda) % k]
            RCr.append(autocorr_sum / k)

        return RCr
