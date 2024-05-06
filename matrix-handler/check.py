import numpy as np
import matplotlib.pyplot as plt

import sys
import json

class PolynomialCalculator:
    def __init__(self, degree, first_digit, second_digit):
        self.degree = degree
        self.first_digit = first_digit
        self.second_digit = second_digit
        self.binary_representation = self.octal_to_binary()

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])

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
        #print(f"Ступінь {s}: {self.degree}")
        #print(f"Поліном {s}: {self.first_digit} {self.second_digit}")

        #print(f"Двійкове представлення {s}: {self.binary_representation}")
        print("Matrix", s)
        #print(f"Період {s}: {(2 ** self.degree - 1)}")
        print(self.__str__())


class S:
    def __init__(self, rows, columns, i, j):
        self.rows = rows
        self.columns = columns
        self.matrix = np.matrix([[0] * columns for _ in range(rows)])
        self.current_index = 0
        self.r = 1
        self.i = i
        self.j = j
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

def val(degreeA, first_digitA, degreeB, first_digitB):
    denominator = gcd(power(degreeA), power(degreeB))
    if denominator != 1:
        return True

    numerator = power(degreeA)
    denominator = gcd(numerator, first_digitA)
    result = numerator / denominator
    if result != numerator:
        return True

    numerator = power(degreeB)
    denominator = gcd(numerator, first_digitB)
    result = numerator / denominator
    if result != numerator:
        return True

    return degreeA > degreeB

def power(n):
    return 2 ** n - 1

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def visualization(acf, r):
    plt.figure(figsize=(14, 6))
    plt.plot(range(len(acf)), acf, linestyle='-')
    plt.title(f'Function {r - 1 }')
    plt.grid(True)

    # Додамо більш детальну шкалу з боку графіка
    plt.minorticks_on()
    plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
    plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

    plt.show()

def main():
    i_ = [1, 2, 3, 2, 3, 1, 3, 2,  3, 2, 4, 2, 1, 3, 4,  1, 4, 5]
    j_ = [8, 3, 7, 2, 8, 1, 4, 11, 3, 2, 4, 1, 5, 3, 10, 2, 4, 5]
    
    n_ = [5, 3, 3, 5, 4, 2, 4, 6,  3, 2, 5, 2, 2, 5, 4,  3, 4,  5]
    m_ = [8, 5, 7, 6, 9, 7, 5, 11, 8, 3, 7, 9, 5, 9, 11, 10, 7, 11]

    second_digit_A = ["45", "13", "13", "45", "23", "7", "23", "103", "13", "7", "45", "7", "7", "45", "23", "13", "23", "45"]
    second_digit_B = ["433", "45", "211", "103", "1021", "211", "45", "4005", "433", "13", "211", "1021", "45", "1021", "4005", "2011", "211", "4005"]
    
    matrices_dict = {}

    for index in range(len(i_)):
        i = i_[index] - 1
        j = j_[index] - 1
        degreeA = n_[index]
        degreeB = m_[index]
        second_digitA = second_digit_A[index]
        second_digitB = second_digit_B[index]
        
        if val(degreeA, 1, degreeB, 1):
            print("Error")
            return
        
        A = PolynomialCalculator(degreeA, 1, second_digitA)
        A.build_polynomial_matrix(True)

        B = PolynomialCalculator(degreeB, 1, second_digitB)
        B.build_polynomial_matrix(False)

        MatrixS = S(degreeA, degreeB, i, j)

        while MatrixS.r <= MatrixS.rows:
            MatrixS.add_one_to_diagonal()
            sub = MatrixS.calculate(A.matrix, B.matrix)

        matrices_dict[str((degreeA, degreeB))] = [A.matrix, B.matrix, sub]

    # Dumping the dictionary to JSON
    with open("matrices.json", "w") as json_file:
        json.dump(matrices_dict, json_file, default=str)
        
        
if __name__ == "__main__":
    main()
    
    


                
                #print("Matrix S", MatrixS.r)
                #print("Період послідовності", MatrixS.T)
                #print("Вага Хемінгу", #MatrixS.hamming_weight())
                #acf = MatrixS.get_acf()
                # print(acf)
                #visualization(acf, MatrixS.r)
                
                            # print(f"degreeA = {degreeA}")
            # print(f"first_digitA = {first_digitA}")
            # print(f"second_digitA = {second_digitA}")

            # print(f"degreeB = {degreeB}")
            # print(f"first_digitB = {first_digitB}")
            # print(f"second_digitB = {second_digitB}")
            
            
                
    # degreeA = 5
    # first_digitA = 3
    # second_digitA = "75"

    # degreeB = 11
    # first_digitB = 1
    # second_digitB = "4005"