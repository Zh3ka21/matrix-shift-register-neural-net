from django.shortcuts import render

# Create your views here.
def base(request):
    return render(request, 'generators/home.html')

def msr(request):
    return render(request, 'generators/msr.html')

def srwf(request):
    return render(request, 'generators/srwf.html')



