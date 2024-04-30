import json
import numpy as np
import re

from helpers.utils import val, gcd, power

# Extracting data from json 
with open('irreducible_polynoms.json') as f:
    data = json.load(f)
    

class PolynomialCalculator:
    def __init__(self, degree, first_digit, second_digit):
        self.degree = degree
        self.first_digit = first_digit
        self.second_digit = second_digit
        self.binary_representation = self.octal_to_binary()

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])

    def get_matrix(self):
        return self.matrix

    def octal_to_binary(self):
        decimal_number = int(self.second_digit, 8)
        binary_number = bin(decimal_number)[2:]
        return binary_number

    def build_polynomial_matrix(self, boolean):
        if boolean:
            binary_ = self.binary_representation[1:]
            n = len(binary_)
            matrix = [[int(digit) for digit in binary_]]

            for i in range(0, n - 1):
                row = [0] * n
                row[i] = 1
                matrix.append(row)
            self.matrix = matrix
        else:
            binary_ = self.binary_representation[1:]
            n = len(binary_)
            matrix = [[0] * n for _ in range(n)]
            reversed_number = int(str(binary_)[::-1])

            for i in range(n - 1):
                matrix[i][i + 1] = 1
                matrix[i][0] = int(reversed_number) % 10
                reversed_number //= 10

            matrix[n - 1][0] = int(reversed_number)
            self.matrix = matrix

    def display(self, s):
        print(f"Ступінь {s}: {self.degree}")
        print(f"Поліном {s}: {self.first_digit} {self.second_digit}")

        print(f"Двійкове представлення {s}: {self.binary_representation}")
        print("Матриця", s)
        print(f"Період {s}: {(2 ** self.degree - 1)}")
        print(self.__str__())


class S:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.matrix = np.matrix([[0] * columns for _ in range(rows)])
        self.current_index = 0
        self.r = 1
        self.i = 1
        self.j = 1
        self.T = power(self.rows) * power(self.columns)

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])

    def add_diagonal_ones(self):
        min_dimension = min(self.rows, self.columns)
        for i in range(min_dimension):
            self.matrix[i, i] = 1

    def add_one_to_diagonal(self):
        min_dimension = min(self.rows, self.columns)
        if self.current_index < min_dimension:
            self.matrix[self.current_index, self.current_index] += 1
            self.current_index = (self.current_index + 1) % self.rows

    def hamming_weight(self):
        return (2 ** self.r - 1) * (2 ** (self.columns + self.rows - self.r - 1))

    def calculate(self, A, B):
        self.r += 1
        limit = np.matrix(self.matrix.copy())
        subsequence = []
        while True:
            self.matrix = ((np.matrix(A) * self.matrix) % 2 * np.matrix(B)) % 2
            subsequence.append(self.matrix[self.i, self.j])
            if np.all(self.matrix == limit):
                self.matrix = limit
                self.up_subsequence = self.update(subsequence)
                return "".join(map(str, subsequence))

    def update(self, sub):
        return [-1 if num == 1 else 1 for num in sub]

    def get_acf(self):
        RCr = []

        for tilda in range(self.T - 1):
            autocorr_sum = 0
            for t in range(self.T - 1):
                autocorr_sum += self.up_subsequence[t] * self.up_subsequence[(t + tilda) % (self.T - 1)]
            RCr.append(autocorr_sum / (self.T))

        return RCr

def save_matrices_to_file(matrices, filename):
    with open(filename, 'w') as file:
        for matrix in matrices:
            for row in matrix:
                file.write(','.join(map(str, row)) + '\n')
            file.write('\n')  # Separate matrices by a blank line


def main():            
    # Appending to list with data
    parameters_list = []
    for degree, values in data.items():
        for dictionary in values:
            for key, value in dictionary.items():
                first_digit = int(key)
                second_digit = int(re.findall(r'\d+', value)[0])
                parameters_list.append((int(degree), first_digit, second_digit))

    # Create lists to store matrices A and B
    matrices_A = []
    matrices_B = []

    # Creating matrices
    for i in range(len(parameters_list) - 1):
        degreeA, first_digitA, second_digitA = parameters_list[i]
        degreeB, first_digitB, second_digitB = parameters_list[i + 1]
        
        if val(degreeA, first_digitA, degreeB, first_digitB):
            print("Error")
            continue
        
        A = PolynomialCalculator(degreeA, first_digitA, str(second_digitA))
        A.build_polynomial_matrix(True)
        B = PolynomialCalculator(degreeB, first_digitB, str(second_digitB))
        B.build_polynomial_matrix(False)
        
        matrices_A.append(A.get_matrix())
        matrices_B.append(B.get_matrix())

    # Save matrices A to file
    save_matrices_to_file(matrices_A, 'matrices_A.txt')

    # Save matrices B to file
    save_matrices_to_file(matrices_B, 'matrices_B.txt')



        
        
        #MatrixS = S(degreeA, degreeB)
        
        #print("Період послідовності", MatrixS.T)
        #while MatrixS.r <= MatrixS.rows:
        #    MatrixS.add_one_to_diagonal()
        #    print("Матриця S", MatrixS.r)
        #    print(MatrixS.__str__())
        #    print("Вага Хемінгу", MatrixS.hamming_weight())
        #    sub = MatrixS.calculate(A.matrix, B.matrix)
        #    print(sub)
        #    acf = MatrixS.get_acf()
        #    # print(acf)
        #    #visualization(acf, MatrixS.r)


if __name__ == "__main__":
    main()