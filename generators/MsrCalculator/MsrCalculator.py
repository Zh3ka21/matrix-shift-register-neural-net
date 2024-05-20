from ..models import Polynomial
import numpy as np
from ..utils import power, lcm


class MsrCalculator:

    def calculate_msr(self, polynomialFirst: Polynomial, polynomialSecond: Polynomial, i:int, j: int, r: int):
        listResult = {}
        resultFirst = {}
        resultSecond = {}
        print(i, j)
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
        matrix, current_index, sequence, binary_sequence = self.get_S(r, rows, columns, matrix,
                                                                      current_index, resultFirst['structure_matrix'],
                                                                      resultSecond['structure_matrix'], i, j)

        listResult['matrixS'] = matrix
        listResult['sequence'] = sequence
        listResult['binary_sequence'] = binary_sequence
        listResult['resultFirst'] = resultFirst
        listResult['resultSecond'] = resultSecond
        resultFirst['T'] = power(rows)
        resultSecond['T'] = power(columns)
        listResult['T_e'] = lcm(resultFirst['T'], resultSecond['T'])
        listResult['T_r'] = len(sequence)
        listResult['hg_e'] = self.hamming_weight(columns, rows, r)
        listResult['hg_r'] = len([i for i in sequence if i == 1])
        listResult['acf'] = self.get_acf(listResult['T_r'], listResult['binary_sequence'])
        return listResult

    @staticmethod
    def get_S(r, rows, columns, matrix, current_index, A, B, index, jndex):
        listMatrix = []
        for i in range(0, r):
            matrix, current_index = MsrCalculator.add_one_to_diagonal(rows, columns, matrix, current_index)
        print(index, jndex)
        sequence = MsrCalculator.get_sequence(A, B, matrix, index, jndex, listMatrix)
        binary_sequence = MsrCalculator.get_binary_sequence(sequence)
        return listMatrix, current_index, sequence, binary_sequence

    @staticmethod
    def get_sequence(A, B, matrix, i, j, matrixR):
        limit = np.matrix(matrix.copy())
        subsequence = []
        while True:
            matrixR.append(matrix.tolist())
            subsequence.append(int(matrix[i, j]))
            matrix = ((np.matrix(A) * matrix) % 2 * np.matrix(B)) % 2
            if np.all(matrix == limit):
                return subsequence

    @staticmethod
    def get_binary_sequence(sub: list[int]):
        return [-1 if num == 1 else 1 for num in sub]

    @staticmethod
    def add_one_to_diagonal(rows: int, columns: int, matrix, current_index):
        min_dimension = min(rows, columns)
        if current_index < min_dimension:
            matrix[current_index, current_index] = 1
            current_index = (current_index + 1) % rows

        return (matrix, current_index)

    @staticmethod
    def hamming_weight(columns: int, rows: int, r: int):
        return (2 ** r - 1) * (2 ** (columns + rows - r - 1))

    @staticmethod
    def octal_to_binary(second_digit: int):
        decimal_number = int(str(second_digit), 8)
        binary_number = bin(decimal_number)[2:]
        return [int(digit) for digit in binary_number]

    @staticmethod
    def get_structure_matrix(boolean: bool, binary_representation: list[int]):
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

    @staticmethod
    def get_acf(T, up_subsequence):
        RCr = []
        for tilda in range(T):
            autocorr_sum = 0
            for t in range(T - 1):
                autocorr_sum += up_subsequence[t] * up_subsequence[(t + tilda) % (T - 1)]
            RCr.append(autocorr_sum / (T))

        return RCr