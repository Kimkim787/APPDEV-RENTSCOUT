from django.shortcuts import render, redirect
from .models import ScoutUser, Building, Highlights, Room, RoomImage, Policies
from .forms import (EmailAuthenticationForm, BuildingForm, UserLoginForm, 
                    ScoutUserCreationForm, RoomForm, RoomImageForm
                    )
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required


from django.views import View
from django.db.models import Q
from django.http import JsonResponse
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
    form = BuildingForm(instance = building)
    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            updated = form.save(commit = False)
            updated.save()
            return redirect('building_info', pk)
        
    context = {'form': form, 'page':page, }
    return render(request, 'RentScout/create_building.html', context)

@login_required
def building_info(request, pk):
    building = Building.objects.get(buildingid = pk)
    highlights = Highlights.objects.filter(buildingid = building)
    rooms = Room.objects.filter(building_id = building)
    room_images = RoomImage.objects.all()
    policies = Policies.objects.filter(buildingid = building)
    roomform = RoomForm()
    photoform = RoomImageForm()

    context = {'building':building, 'highlights': highlights, 'room_images': room_images,
               'rooms':rooms, 'policies':policies, 'roomform':roomform,
                'photoform':photoform, }
    
    return render(request, 'RentScout/building.html', context)

def building_del(request, pk):
    building = Building.objects.get(buildingid = pk)
    building.delete()
    return redirect('home')

def room_create(request, buildingID):
    building = Building.objects.get(buildingid = buildingID)

    if request.method == 'POST':
        room = RoomForm(request.POST)
        if room.is_valid():
            newroom = room.save(commit=False)
            newroom.building_id = building
            newroom.save()
        else:
            print(room.errors)
            print("failed to create room")
            messages.error(request, "Failed to create room")
    
    return redirect('building_info', building.buildingid )


def room_update(request):
    if request.method =='POST':
        room_id = request.POST.get('room_id')
        room = Room.objects.get(roomid = room_id)
        tryroom = RoomForm(request.POST, instance = room)
        if tryroom.is_valid():
           updated_room = tryroom.save(commit=False)
           updated_room.save()
           print('Successfully updated room', room.room_name)
           messages.success(request, 'Successfuly updated room')
           return redirect('building_info', room.building_id.buildingid)
        else:
            print("Failed to update room", tryroom.errors)
            messages.error(request, 'Failed to update room')
            return redirect('building_info', room.building_id.buildingid)

# ROOM PHOTOS
def room_photo_upload(request):
    print('rooom photo upload')
    if request.method == 'POST':
        print('request post')
        photoform = RoomImageForm(request.POST, request.FILES)
        roomid = request.POST.get('roomid')
        if photoform.is_valid():
            print('valid photo form')
            newphoto = photoform.save(commit=False)
            newphoto.save()

    return redirect('building_info', roomid)


@login_required( login_url = 'signin' )
def home(request):
    return render(request, 'RentScout/home.html', {})


class get_room_data(View):
    print('room_data')
    def get(self, request):
        query = request.GET.get('primary_key', '') # query comes from ajax
        print(query)
        if query:
            try:
                room = Room.objects.get(roomid = query)

                room_data = {
                    'roomid': room.roomid,
                    'room_name': room.room_name,
                    'person_free': room.person_free,
                    'current_male': room.current_male,
                    'current_female': room.current_female,
                    'price': room.price,
                    'room_size': room.room_size,
                    'shower': room.shower,
                    'priv_bathroom': room.priv_bathrooom,
                    'public_bathroom': room.public_bathroom,
                    'AC': room.AC,
                    'wardrobe': room.wardrobe,
                    'kitchen': room.kitchen,
                    'bed': room.bed,
                    'double_deck': room.double_deck,
                    'free_wifi': room.free_wifi,
                }

                return JsonResponse(room_data, safe =  False)

            except Room.DoesNotExist:
                return JsonResponse({'error': 'Room not found'}, status = 404) # Page not found
        else:
            return JsonResponse({'error': 'No query provided'}, status = 400) # Bad reqeust

class get_room_images(View):
    def get(self, request):
        query = request.GET.get('roomid', '')
        if query:
            
            try:
                photos = list(RoomImage.objects.filter(
                roomid = query).values_list('room_img'))
                image_obj = {}
                for index, photo in enumerate(photos, start=0):
                    image_obj[index] = photo  
                
                print(image_obj)
                return JsonResponse(image_obj, safe=False)
            except:
                return JsonResponse({'error': 'No images found'}, status = 404)
        else:
            return JsonResponse({'error': 'Did not receive a query'}, status = 405)
        
