from django.shortcuts import render, redirect
from .models import ScoutUser
from .forms import EmailAuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

# Create your views here.

def get_user_backend(user):
    if isinstance(user, ScoutUser):
        return 'RentScout.auth_backends.ScoutUserBackend'

    return None

def scoutuser_signup(request):
    page = 'signup'
    form = EmailAuthenticationForm()
    
    if request.method == "POST":
        form = EmailAuthenticationForm()
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = email, password = password)
            if user is not None and isinstance(user, ScoutUser):
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Please complete the form')
    
    return render(request, '', {})

def scoutuser_login(request):
    form = EmailAuthenticationForm()
    
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data = request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = email, password = password)
            if user is not None and isinstance(user, ScoutUser):
                login(request, user)
                return redirect('')
            else:
                messages.error(request, 'User does not exist')
    else:
        messages.error(request, 'Invalid email or password')

    return render(request, '')


def home(request):
    return render(request, 'RentScout/home.html', {})
