from django.shortcuts import render, redirect
from .models import ScoutUser, Building
from .forms import EmailAuthenticationForm, BuildingForm
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

# HANDLES BUILDING CREATION
def create_building(request, ownerid):
    form = BuildingForm()
    scoutuser = ScoutUser.objects.get(userid = ownerid)
    if request.method == 'POST':
        form = BuildingForm(request.POST, request.FILES)
        if form.is_valid():
            newbuilding = form.save(commit = False)
            newbuilding.building_owner = scoutuser
            newbuilding.save()
            return redirect('')
    
    context = {'form': form, }
    return render(request, '', context)

def update_building(request, pk):
    building = Building.objects.get(buildingid = pk)
    form = BuildingForm(instance = pk)
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            updated = form.save(commit = False)
            updated.save()
            return redirect('')
        
    context = {'form', form}
    return render(request, '', context)

def home(request):
    return render(request, 'RentScout/home.html', {})
