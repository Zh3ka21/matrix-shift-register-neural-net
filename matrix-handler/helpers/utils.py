
def val(degreeA, first_digitA, degreeB, first_digitB):
    denominator = gcd(power(degreeA), power(degreeB))
    if denominator != 1:
        print("gcd not 1")
        return True

    numerator = power(degreeA)
    denominator = gcd(numerator, first_digitA)
    result = numerator / denominator
    if result != numerator:
        print("TA not max")
        return True

    numerator = power(degreeB)
    denominator = gcd(numerator, first_digitB)
    result = numerator / denominator
    if result != numerator:
        print("TB not max")
        return True

    return degreeA >= degreeB

def power(n):
    return 2 ** n - 1

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# def visualization(acf, r):
#     plt.figure(figsize=(14, 6))
#     plt.plot(range(len(acf)), acf, linestyle='-')
#     plt.title(f'Function {r - 1 }')
#     plt.grid(True)

#     # Додамо більш детальну шкалу з боку графіка
#     plt.minorticks_on()
#     plt.grid(which='major', linestyle='-', linewidth='0.5', color='black')
#     plt.grid(which='minor', linestyle=':', linewidth='0.5', color='gray')

#     plt.show()