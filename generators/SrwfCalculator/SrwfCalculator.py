from django.http import JsonResponse
from ..models import Polynomial
from .utils import find_gcd

class SrwfCalculator:

    @staticmethod
    def get_polynomials(request):
        selected_degree = request.GET.get('degree')
        polynomials = Polynomial.objects.filter(degree=selected_degree).values('id', 'first_number', 'second_number', 'letter')
        return JsonResponse(list(polynomials), safe=False)


    def calculate_srwf(self, polynomial_id, selected_number):
        polynomial = Polynomial.objects.get(pk=polynomial_id)
        result = {}
        result['structure_matrix'], second_digit_binary= self.get_structure_matrix(polynomial)
        result['state'] = self.get_state(polynomial, selected_number, result['structure_matrix'])
        result['sequence'] = self.get_sequence(result['state'])
        result['binary_sequence'] = self.get_binary_sequence(result['sequence'])
        result['hg'], result['T_e'], result['T_r'] = self.get_property(polynomial, result['sequence'])
        result['poly'] = self.get_poly(second_digit_binary)
        return result

    @staticmethod
    def get_structure_matrix(polynomial: Polynomial):
        decimal_number = int(str(polynomial.second_number), 8)
        binary_number = bin(decimal_number)[2:]
        second_digit_binary = [int(bit) for bit in binary_number][1:]

        matrix = [[int(digit) for digit in second_digit_binary]]
        for i in range(polynomial.degree - 1):
            row = [0] * polynomial.degree
            row[i] = 1
            matrix.append(row)

        return matrix, second_digit_binary

    @staticmethod
    def get_state(polynomial: Polynomial, selected_number: int, matrix: list[list[int]]):
        binary_representation = format(selected_number, f'0{int(polynomial.degree)}b')
        lst = [int(i) for i in binary_representation]
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
                break
            matrices.append(result_array)

        return matrices

    @staticmethod
    def get_sequence(matrices: list[list[int]]):
        sequence = []
        for matrice in matrices:
            sequence.append(matrice[-1])

        return sequence

    @staticmethod
    def get_binary_sequence(sequence: list[int]):
        return [1 if i == 0 else -1 for i in sequence]

    @staticmethod
    def get_property(polynomial: Polynomial, sequence: list[int]):
        T = pow(2, polynomial.degree) - 1
        hg = len([i for i in sequence if i == 1])
        T_e = T / find_gcd(T, polynomial.first_number)
        T_r = len(sequence)
        return (hg, T_e, T_r)

    @staticmethod
    def get_poly(second_digit_binary: list[int]):
        poly = ''
        binary_representation_copy = second_digit_binary.copy()
        binary_representation_copy.insert(0, 1)
        for i in range(len(binary_representation_copy)):
            if binary_representation_copy[i] == 1:
                poly += f'x^{len(binary_representation_copy) - 1 - i}'

        return poly if poly else '0'
