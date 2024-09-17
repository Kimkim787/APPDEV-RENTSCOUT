from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def home(request):
    return render(request, 'RentScout/home.html', {})

def signinpage(request):
    return render(request, 'RentScout/signin.html', {})