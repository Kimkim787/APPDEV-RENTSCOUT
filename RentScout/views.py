from django.shortcuts import render, redirect
from .models import (ScoutUser, Building, Highlights, Room, 
                     RoomImage, Policies, Feedback, ScoutUser_Landlord,
                     
                    )
from .forms import (EmailAuthenticationForm, BuildingForm, UserLoginForm, 
                    ScoutUserCreationForm, RoomForm, RoomImageForm, FeedBackForm,
                    LandlordUserCreationForm
                    )
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist as ObjException

from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages

import logging
logger = logging.getLogger(__name__)

def get_user_backend(user):
    if isinstance(user, ScoutUser):
        return 'RentScout.auth_backends.ScoutUserBackend'
    
    if isinstance(user, ScoutUser_Landlord):
        return 'RentScout.auth_backends.ScoutUserLandlordBackend'
    
    return None

def scoutuser_signup(request):
    form = ScoutUserCreationForm()

    if request.method == "POST":
        role = request.POST.get('role')

        if role == 'Boarder':
            form = ScoutUserCreationForm(request.POST)

            if form.is_valid():
                user = form.save()
                backend = get_user_backend(user)
                login(request, user, backend)
                return redirect('home')
            
            else:
                messages.error(request, 'Please enter a valid email or password')
        
        elif role == 'Landlord':
            form = LandlordUserCreationForm(request.POST)

            if form.is_valid():
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
        email = request.POST.get('username')
        password = request.POST.get('password')

        print(email)
        print(password)

        form = EmailAuthenticationForm(request, data = request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            try:
                user = authenticate(request, username = email, password = password)
            except:
                user = UserLoginForm(request, data=request.POST)
            
            backend = get_user_backend(user)

            if user is not None and isinstance(user, ScoutUser):
                login(request, user, backend)
                return redirect('home')
            elif user is not None and isinstance(user, ScoutUser_Landlord):
                login(request, user, backend)
                return redirect('home')
            else:
                print('Invalid email or password')
                messages.error(request, 'Invalid email or password')
        else:
            print(form.errors)
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
    building_id = building.buildingid
    if request.method == 'POST':
        form = BuildingForm(request.POST, instance=building)
        if form.is_valid():
            updated = form.save(commit = False)
            updated.save()
            return redirect('building_info', pk)
        else:
            print(form.errors)
    context = {'form': form, 'page':page, 'buildingid': building_id}
    return render(request, 'RentScout/create_building.html', context)

@login_required
def building_info(request, pk):
    building = Building.objects.get(buildingid = pk)
    try:
        highlights = Highlights.objects.get(buildingid = building)
    except:
        highlights = None
    rooms = Room.objects.filter(building_id = building)
    room_images = RoomImage.objects.all()
    policies = Policies.objects.filter(buildingid = building)
    feedbacks = Feedback.objects.filter(boardingid = pk)
    roomform = RoomForm()
    feedbackForm = FeedBackForm()

    context = {'building':building, 'highlights': highlights, 'room_images': room_images,
               'rooms':rooms, 'policies':policies, 'roomform':roomform, 'feedbacks':feedbacks,
               'feedbackform':feedbackForm,
            }
    
    return render(request, 'RentScout/building.html', context)

def building_del(request, pk):
    building = Building.objects.get(buildingid = pk)
    building.delete()
    return redirect('home')

def building_edit(request):

    if not (isinstance(request.user, ScoutUser_Landlord)):
        return redirect(request.META.get('HTTP_REFERER'))

    try:
        buildings = Building.objects.filter(building_owner = request.user)
        photo_form = RoomImageForm()
    except ObjException as e:
        messages.error(request, f'{e}')


    context = {'buildings':buildings, 'photoform': photo_form, }
    return render(request, 'RentScout/edit_building.html', context)

def create_feedback(request):
    if request.method == 'POST':
        feedbackform = FeedBackForm(request.POST)
        if feedbackform.is_valid():
            newfeedback = feedbackform.save(commit = False)
            newfeedback.userid = request.user
            newfeedback.save()
            messages.success(request, "Feedback sent")
            return redirect('building_info', newfeedback.boardingid.buildingid)
        else:
            messages.error(request, "Unable to save feedback")
            
def update_feedback(request, pk):
    if request.method == 'POST':
        print('update feedback POST')
        oldfeedback = Feedback.objects.get(feedbackid = pk)
        feedbackform = FeedBackForm(request.POST, instance=oldfeedback)

        if feedbackform.is_valid():
            print('FORM IS VALID')
            updated = feedbackform.save(commit=False)
            updated.save()
            messages.success(request, "Feedback updated")
            return redirect('building_info', updated.boardingid.buildingid)
        else:
            messages.error(request, "Unable to update feedback")
            print(feedbackform.errors)

            return redirect('building_info', oldfeedback.boardingid.buildingid)


# ROOM THINGS
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
        if photoform.is_valid():
            print('valid photo form')
            newphoto = photoform.save(commit=False)
            newphoto.save()
        return redirect('edit_building')

def room_edit_photo(request, pk):
    images = RoomImage.objects.filter(roomid = pk)
    rooms = Room.objects.filter(building_id__building_owner = request.user)
    
    # For image upload
    photoform = RoomImageForm()

    context = { 'images': images, 'rooms':rooms, 'photoform':photoform, 
                'room_id': pk, }
    return render(request, 'RentScout/edit_room_photo.html', context)

def room_delete_photo(request):
    if request.method == 'POST':
        img_id = request.POST.get("img_id")
        image = RoomImage.objects.get(room_imgID = img_id)
        room_id = image.roomid.roomid
        print(room_id)
        image.delete()
        return redirect('edit_photo', room_id)

@login_required( login_url = 'signin' )
def home(request):
    return render(request, 'RentScout/home.html', {})


class get_rooms(View):
    def get(self,request):
        query = request.GET.get('building_id', '')
        if query:
            try:
                rooms = Room.objects.filter(building_id = query)
                room_data = []
                for room in rooms:
                    room_data.append({
                        'roomid': room.roomid,
                        'room_name': room.room_name,
                    })
                    
                return JsonResponse({"room_data":room_data })
            
            except Room.DoesNotExist:
                messages.error(request, 'Error 404: Rooms Not Found')
                JsonResponse({'error': 'Rooms Not Found'}, status=404)
        else:
            messages.error(request, 'Error 405: Bad request')
            JsonResponse({'error': 'Bad request'}, status=405)



class get_room_data(View):
    def get(self, request):
        query = request.GET.get('primary_key', '') # query comes from ajax
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
                room = Room.objects.get(roomid = query)
                photos = RoomImage.objects.filter(roomid = query)
                image_list = []
                for photo in photos:
                    image_list.append({
                        'photo_id': photo.room_imgID,
                        'photo_url': photo.room_img.url
                    })
                
                response_data = {
                    "image_list":image_list,
                    'room_name': room.room_name 
                }
                return JsonResponse(response_data)
            except Exception as e:
                return JsonResponse({'error': e}, status = 404)
        else:
            return JsonResponse({'error': 'Did not receive a query'}, status = 405)

class del_room_photo_view(View):

    def post(self, request):
        query = request.POST.get('photo_id', '')
        if query:
            try:
                img = RoomImage.objects.get(room_imgID = query)
                img.delete()
                return JsonResponse({'message': "Image deleted"}, status = 200)
            except RoomImage.DoesNotExist:
                return JsonResponse({"error": "Room Image Does not exist"}, status = 404)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status = 500)
        else:
            return JsonResponse({'error': "Did not receive query data"})
        
class upload_room_photo_view(View):
    def post(self, request):
        print("Processing Photo Upload")
        try:
            roomid = request.POST.get('roomid')
            photoform = RoomImageForm(request.POST, request.FILES)
            room = Room.objects.get(roomid = roomid)
            if photoform.is_valid():
                print('valid photo form')
                newphoto = photoform.save(commit=False)
                newphoto.roomid = room
                newphoto.save()
                return JsonResponse({'message': 'Photo uploaded'}, status = 200)
        except Exception as e:
            return JsonResponse({'error', 'Error photo upload'}, status = 500)
        













