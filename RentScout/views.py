from django.shortcuts import render, redirect
from .models import ScoutUser, Building
from .forms import EmailAuthenticationForm, BuildingForm, UserLoginForm, ScoutUserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def get_user_backend(user):
    if isinstance(user, ScoutUser):
        return 'RentScout.auth_backends.ScoutUserBackend'

    return None

def scoutuser_signup(request):
    page = 'signup'
    form = ScoutUserCreationForm()
    
    if request.method == "POST":
        print('tried to signup')
        form = ScoutUserCreationForm(request.POST)
        print(form)
        if form.is_valid():
            print('form is valid')
            user = form.save()
            backend = get_user_backend(user)
            login(request, user, backend)
            return redirect('home')
        else:
            messages.error(request, 'Please enter a valid email or password')
            
    context = {'form': form, }
    return render(request, 'RentScout/signup.html', context)

def scoutuser_login(request):
    form = EmailAuthenticationForm()
    
    if request.method == 'POST':
        print('post request')
        form = EmailAuthenticationForm(request, data = request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username = email, password = password)
            if user is not None and isinstance(user, ScoutUser):
                login(request, user)
                print('login success')
                return redirect('home')
            else:
                print('Invalid email or password')
                messages.error(request, 'Invalid email or password')
        else:
            print('User does not exist')
            messages.error(request, 'User does not exist')

    context = {'form': form}
    return render(request, 'RentScout/signin.html', context)

def scoutuser_logout(request):
    logout(request)
    return redirect('home')

# HANDLES BUILDING CREATION
def create_building(request):
    page = "newbuilding"
    form = BuildingForm()
    if request.method == 'POST':
        form = BuildingForm(request.POST, request.FILES)
        if form.is_valid():
            newbuilding = form.save(commit = False)
            newbuilding.building_owner = request.user
            newbuilding.save()
            return redirect('home')
    
    context = {'form': form, 'page':page, }
    return render(request, 'RentScout/create_building.html', context)

def update_building(request, pk):
    page = "update"
    building = Building.objects.get(buildingid = pk)
    form = BuildingForm(instance = pk)
    if request.method == 'POST':
        form = BuildingForm(request.POST)
        if form.is_valid():
            updated = form.save(commit = False)
            updated.save()
            return redirect('home')
        
    context = {'form': form, 'page':page, }
    return render(request, '', context)

def building_info(request, pk):
    building = Building.objects.get(buildingid = pk)

    context = {'building':building, }
    return render(request, 'RentScout/building.html', context)

def home(request):
    return render(request, 'RentScout/home.html', {})

# def signinpage(request):
#     return render(request, 'RentScout/signin.html', {})