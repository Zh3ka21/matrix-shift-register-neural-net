from django.http import JsonResponse
from ..models import Polynomial
import numpy as np
from .utils import power


class MsrCalculator:

    def calculate_msr(self, polynomialFirst, polynomialSecond):
        listResult = {}
        resultFirst = {}
        resultSecond = {}

        secondDigitBinaryFirst = self.octal_to_binary(polynomialFirst.second_number)
        resultFirst['structure_matrix'] = self.get_structure_matrix(True, secondDigitBinaryFirst)
        resultFirst['poly'] = self.get_poly(secondDigitBinaryFirst)

        secondDigitBinarySecond = self.octal_to_binary(polynomialSecond.second_number)
        resultSecond['structure_matrix'] = self.get_structure_matrix(False, secondDigitBinarySecond)
        resultSecond['poly'] = self.get_poly(secondDigitBinarySecond)

        rows = len(resultFirst['structure_matrix'])
        columns = len(resultSecond['structure_matrix'])
        matrix = np.matrix([[0] * columns for _ in range(rows)])

        current_index = 0
        i = 1
        j = 1
        r = 2
        matrix, current_index, sequence, binary_sequence= self.get_S(r, rows, columns, matrix, current_index, resultFirst['structure_matrix'], resultSecond['structure_matrix'])

        listResult['matrixS'] = matrix
        listResult['sequence'] = sequence
        listResult['binary_sequence'] = binary_sequence
        listResult['resultFirst'] = resultFirst
        listResult['resultSecond'] = resultSecond
        resultFirst['T'] = power(rows)
        resultSecond['T'] = power(columns)
        listResult['T_e'] = resultFirst['T'] * resultSecond['T']
        listResult['T_r'] = len(sequence)
        listResult['hg_e'] = self.hamming_weight(columns, rows, r)
        listResult['hg_r'] = len([i for i in sequence if i == 1])
        return listResult

    @staticmethod
    def get_S(r, rows, columns, matrix, current_index, A, B):
        binary_sequence = []
        listMatrix = []
        for i in range(0, r):
            matrix, current_index = MsrCalculator.add_one_to_diagonal(rows, columns, matrix, current_index)
        sequence = MsrCalculator.get_sequence(A, B, matrix, 1, 1, listMatrix)
        binary_sequence.append(MsrCalculator.get_binary_sequence(sequence))
        return listMatrix, current_index, sequence, binary_sequence

    @staticmethod
    def get_sequence(A, B, matrix, i, j, matrixR):
        limit = np.matrix(matrix.copy())
        subsequence = []
        while True:
            matrixR.append(matrix.tolist())
            matrix = ((np.matrix(A) * matrix) % 2 * np.matrix(B)) % 2
            subsequence.append(int(matrix[i, j]))
            if np.all(matrix == limit):
                return subsequence

    @staticmethod
    def get_binary_sequence(sub):
        return [-1 if num == 1 else 1 for num in sub]

    @staticmethod
    def add_one_to_diagonal(rows, columns, matrix, current_index):
        min_dimension = min(rows, columns)
        if current_index < min_dimension:
            matrix[current_index, current_index] = 1
            current_index = (current_index + 1) % rows

        return (matrix, current_index)

    @staticmethod
    def hamming_weight(columns, rows, r):
        return (2 ** r - 1) * (2 ** (columns + rows - r - 1))

    @staticmethod
    def octal_to_binary(second_digit):
        decimal_number = int(str(second_digit), 8)
        binary_number = bin(decimal_number)[2:]
        return [int(digit) for digit in binary_number]

    @staticmethod
    def get_structure_matrix(boolean, binary_representation):
        if boolean:
            binary_ = binary_representation[1:]
            n = len(binary_)
            matrix = [[int(digit) for digit in binary_]]

            for i in range(0, n - 1):
                row = [0] * n
                row[i] = 1
                matrix.append(row)
        else:
            binary_ = ''.join(map(str, binary_representation[1:]))
            n = len(binary_)
            matrix = [[0] * n for _ in range(n)]
            reversed_number = int(str(binary_)[::-1])

            for i in range(n - 1):
                matrix[i][i + 1] = 1
                matrix[i][0] = int(reversed_number) % 10
                reversed_number //= 10

            matrix[n - 1][0] = int(reversed_number)

        return matrix

    @staticmethod
    def get_poly(second_digit_binary: list[int]):
        poly = ''
        binary_representation_copy = second_digit_binary.copy()
        binary_representation_copy.insert(0, 1)
        for i in range(len(binary_representation_copy)):
            if binary_representation_copy[i] == 1:
                poly += f'x^{len(binary_representation_copy) - 1 - i} + '

        return poly[:-3] if poly else '0'
