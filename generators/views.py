from django.core.exceptions import ValidationError
from django.shortcuts import render
from .models import Polynomial
from django.http import JsonResponse
from .SrwfCalculator.SrwfCalculator import SrwfCalculator
from .MsrCalculator.MsrCalculator import MsrCalculator
from .SrwfCalculator.PRNG import BinaryToAverageModel
from .utils import validation, get_polynomials
from django.http import FileResponse

import os
import pandas as pd
from docx import Document


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
    #print(binary_representations_to_predict)   
    predicted_average_numbers = btam.predict(binary_representations_to_predict)
    result["rlst"] = predicted_average_numbers.tolist()
    result['erlst'] = len(predicted_average_numbers.tolist())/sum(predicted_average_numbers.tolist())
    
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
        validate_result, error_message = validation(
            degreeFirst, polynomialFirst.first_number, degreeSecond,                                                    polynomialSecond.first_number
        )
        if validate_result:
            raise ValidationError(error_message)

        cal = MsrCalculator()
        listResult = cal.calculate_msr(polynomialFirst, polynomialSecond, i, j, r)

        btam = BinaryToAverageModel()
        btam.load_model()
        string_sequence = ''.join(map(str, listResult['sequence']))
        binary_representations_to_predict = [string_sequence]
        #print(binary_representations_to_predict)   
        predicted_average_numbers = btam.predict(binary_representations_to_predict)
        listResult["mlst"] = predicted_average_numbers.tolist()
        listResult['emlst'] = len(predicted_average_numbers.tolist())/sum(predicted_average_numbers.tolist())
        
        return JsonResponse({'listResult': listResult})
    except ValidationError as e:
        return JsonResponse({'error': str(e)}, status=400)

def download_excel(request):
    file_name = 'Table.xlsx'
    response = FileResponse(open(file_name, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response

def download_word(request):
    file_name = 'Report.docx'
    response = FileResponse(open(file_name, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    return response

def display_excel(request):
    file_path = 'Table.xlsx'
    
    # Read the Excel file
    xls = pd.ExcelFile(file_path)
    
    # Read the sheets into dataframes
    df1 = pd.read_excel(xls, sheet_name=xls.sheet_names[0])
    df2 = pd.read_excel(xls, sheet_name=xls.sheet_names[1])
    
    # Convert dataframes to HTML
    html_table1 = df1.to_html(classes='table table-striped', index=False)
    html_table2 = df2.to_html(classes='table table-striped', index=False)
    
    return render(request, 'display_excel.html', {'table1': html_table1, 'table2': html_table2})

def display_word(request):
    file_path = 'Report.docx'
    
    # Read the Word document
    doc = Document(file_path)
    
    # Extract text from each paragraph
    paragraphs = [p.text for p in doc.paragraphs]
    
    return render(request, 'display_word.html', {'paragraphs': paragraphs})