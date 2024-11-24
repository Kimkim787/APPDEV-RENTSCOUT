from django.shortcuts import render, redirect
from .models import (ScoutUser, Building, Highlights, Room, 
                     RoomImage, Policies, Feedback, ScoutUser_Landlord,
                     ScoutUserBookmark, LandlordUserBookmark, AdminUser, BuildingReport,
                     Verification
                    )

from .forms import (EmailAuthenticationForm, BuildingForm, UserLoginForm, 
                    ScoutUserCreationForm, RoomForm, RoomImageForm, FeedBackForm,
                    LandlordUserCreationForm, PoliciesForm, HighlightsForm,
                    ScoutUserProfileForm, LandlordUserProfileForm,
                    ScoutBookmarkForm, LandlordBookmarkForm, ScrapperFile, BuildingReportForm,
                    VerificationForm, 
                    )
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist as ObjException

from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string


import logging, math, csv
from django.core.paginator import Paginator
logger = logging.getLogger(__name__)

def get_user_backend(user):
    if isinstance(user, ScoutUser):
        return 'RentScout.auth_backends.ScoutUserBackend'
    
    if isinstance(user, ScoutUser_Landlord):
        return 'RentScout.auth_backends.ScoutUserLandlordBackend'
    
    if isinstance(user, AdminUser):
        return 'RentScout.auth_backends.AdminUserBackend'
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
                print(form.errors)
                #error(request, 'Please enter a valid email or password')
        
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
            elif user is not None and isinstance(user, AdminUser):
                login(request, user, backend)
                return redirect('home')
            else:
                print('Invalid email or password')
                #error(request, 'Invalid email or password')
        else:
            print(form.errors)
            #error(request, 'User does not exist')

    context = {'form': form}
    return render(request, 'RentScout/signin.html', context)

@login_required(login_url = "signin")
def scoutuser_logout(request):
    logout(request)
    return redirect('home')

# HANDLES BUILDING CREATION
# @login_required(login_url = "signin")
# def create_building(request):

#     if not isinstance(request.user, ScoutUser_Landlord):
#         #error(request, "Must be a landlord user to create Buildings")
#         return redirect(request.META.get('HTTP_REFERER'))
        
#     page = "newbuilding"
#     form = BuildingForm()
#     if request.method == 'POST':
#         form = BuildingForm(request.POST, request.FILES)
#         print(form)
#         if form.is_valid():
#             newbuilding = form.save(commit = False)
#             newbuilding.building_owner = request.user
#             newbuilding.save()
#             return redirect('home')
#         else:
#             print(form.errors)
#     context = {'form': form, 'page':page, }
#     return render(request, 'RentScout/create_building.html', context)

@login_required(login_url = "signin")
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

@login_required(login_url = "signin")
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
    reportform = BuildingReportForm()
    feedbackForm = FeedBackForm()
    verification_status = "Not Verified"

    try:
        verification = Verification.objects.get(buildingid = building)
        verification_status = verification.status
    except Exception as e:
        pass

    context = {'building':building, 'highlights': highlights, 'room_images': room_images,
               'rooms':rooms, 'policies':policies, 'roomform':roomform, 'feedbacks':feedbacks,
               'feedbackform':feedbackForm, 'building_report_form': reportform, 
               'verification': verification_status,
            }
    
    return render(request, 'RentScout/building.html', context)

@login_required(login_url = "signin")
def building_del(request, pk):
    building = Building.objects.get(buildingid = pk)
    building.delete()
    return redirect('home')

@login_required(login_url = "signin")
def building_edit(request):
    # amenity = {}
    if not (isinstance(request.user, ScoutUser_Landlord)):
        return redirect('home')

    try:
        buildings = Building.objects.filter(building_owner = request.user)
        photo_form = RoomImageForm()
        building_form = BuildingForm()
        amenities_form = HighlightsForm()
    except ObjException as e:
        messages.error(request, f'{e}')

    # try:
    #     amenity = Highlights.objects.get(buildingid = buildings)
    # except:
    #     pass
    print(buildings)
    context = {'buildings':buildings, 'photoform': photo_form, 'amenities_form':amenities_form,
               'building_form': building_form, 
            #    'amenity': amenity, 
               }
    return render(request, 'RentScout/edit_building.html', context)

@login_required(login_url = "signin")
def create_building_edit_page(request):
    if not (isinstance(request.user, ScoutUser_Landlord)):
        return redirect('edit_building')

    if request.method == 'POST':
        form = BuildingForm(request.POST, request.FILES)
        if form.is_valid():
            newbuilding = form.save(commit = False)
            newbuilding.building_owner = request.user
            newbuilding.save()
            return redirect('edit_building')
        else:
            print(form.errors)
    return redirect('edit_building')

class building_edit_view(View):
    def get(self, request):
        bldg_id = request.GET.get('bldg_id', '')
        if bldg_id:
            try:
                building = Building.objects.get(buildingid = bldg_id)
                form = BuildingForm(instance = building)
                form_data = {field.name: field.value() for field in form}
                form_data['building_image'] = building.building_image.url if building.building_image else None
                print(form_data)    
                return JsonResponse(form_data, status = 200)
            except Building.DoesNotExist:
                return JsonResponse({"error": "Building does not exist"}, status = 400)
            except Exception as e:
                return JsonResponse({"message": f"{e}"})
        else:
            return JsonResponse({"error": "Did not get Building ID"})
            
    def post(self, request):
        if not (isinstance(request.user, ScoutUser_Landlord)):
            return redirect(request.META.get('HTTP_REFERER'))

        bldg_id = request.POST.get('bldg_id')
        if bldg_id:
            try:
                building = Building.objects.get(buildingid = bldg_id)
                bldg_form = BuildingForm(request.POST,instance = building)
                print(bldg_form)
                if bldg_form.is_valid():
                    print("bldg form is valid")
                    new_bldg = bldg_form.save(commit = False)
                    new_bldg.save()
                    return JsonResponse({'success': f'successfully updated {building.building_name} Building'}, status = 200)
                else:
                    return JsonResponse({"error": 'Form update is invalid'}, status = 500)
            except Building.DoesNotExist:
                return JsonResponse({'error': "Building doesn't exist"}, status = 405)
        else:
            return JsonResponse({'error': "Did not get building id"}, status =405)

class delete_building_view(View):
    def post(self, request):
        try:
            buildingid = request.POST.get('buildingid')
            print('Received building id:', buildingid)  # Debugging line
            
            if not buildingid:
                return JsonResponse({'error': 'Building ID not provided'}, status=400)

            building = Building.objects.get(buildingid=buildingid)
            building.delete()
            #success(request, 'Building successfully deleted')
            return JsonResponse({'success': 'Building successfully deleted'}, status=200)
        
        except Building.DoesNotExist:
            print("Building does not exist")
            return JsonResponse({'error': 'Building does not exist'}, status=404)
        
        except Exception as e:
            print("Error:", e)
            return JsonResponse({'error': f'Unexpected error: {e}'}, status=500)

@login_required(login_url = "signin")
def create_feedback(request):
    if request.method == 'POST':
        feedbackform = FeedBackForm(request.POST)
        if feedbackform.is_valid():
            newfeedback = feedbackform.save(commit = False)
            newfeedback.userid = request.user
            newfeedback.save()
            #success(request, "Feedback sent")
            messages.success(request, "Successfully sent your feedback")
            return redirect('building_info', newfeedback.boardingid.buildingid)
        else:
            messages.error(request, "Unable to save feedback")

@login_required(login_url = "signin")   
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

@login_required(login_url = "signin")
def room_create(request, buildingID):
    building = Building.objects.get(buildingid = buildingID)

    if request.method == 'POST':
        room = RoomForm(request.POST)
        if room.is_valid():
            newroom = room.save(commit=False)
            newroom.building_id = building
            newroom.save()
            messages.success(request, f"{newroom.room_name} has been successfully created")
        else:
            print(room.errors)
            print("failed to create room")
            messages.error(request, "Please complete the form before saving")
    
    return redirect('building_info', building.buildingid )

@login_required(login_url = "signin")
def room_update(request):
    if request.method =='POST':
        room_id = request.POST.get('room_id')
        room = Room.objects.get(roomid = room_id)
        tryroom = RoomForm(request.POST, instance = room)
        if tryroom.is_valid():
           updated_room = tryroom.save(commit=False)
           updated_room.save()
           print('Successfully updated room', room.room_name)
           messages.success(request, 'Successfully updated room')
           return redirect('building_info', room.building_id.buildingid)
        else:
            print("Failed to update room", tryroom.errors)
            messages.error(request, 'Please complete the form before saving')
            return redirect('building_info', room.building_id.buildingid)

# ROOM PHOTOS
@login_required(login_url = "signin")
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

@login_required(login_url = "signin")
def room_edit_photo(request, pk):
    images = RoomImage.objects.filter(roomid = pk)
    rooms = Room.objects.filter(building_id__building_owner = request.user)
    
    # For image upload
    photoform = RoomImageForm()

    context = { 'images': images, 'rooms':rooms, 'photoform':photoform, 
                'room_id': pk, }
    return render(request, 'RentScout/edit_room_photo.html', context)

@login_required(login_url = "signin")
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


@login_required(login_url='signin')
def user_profile(request):
    if isinstance(request.user, ScoutUser):
        form = ScoutUserProfileForm()
        user_data = ScoutUser.objects.get(userid = request.user.userid)
        context = {'form': form, 'user_data': user_data}
    elif isinstance(request.user, ScoutUser_Landlord):
        form = LandlordUserProfileForm()
        user_data = ScoutUser_Landlord.objects.get(userid = request.user.userid)
        context = {'form': form, 'user_data': user_data}
    elif isinstance(request.user, AdminUser):
        # Partial: View admin job status. daily actions.
        form = ""
        user_data = AdminUser.objects.get(userid = request.user.userid)
        context = {'form': form, 'user_data': user_data}
    return render(request, 'RentScout/user_profile.html', context)

# no login required
@login_required(login_url = "signin")
def user_profile_admin_access(request, userid):
    if isinstance(request.user, AdminUser):
        user_data = ScoutUser_Landlord.objects.get(userid = request.user.userid)
        context = {'user_data': user_data}
        return render(request, 'RentScout/user_profile.html', context)
    else:
        return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url = "signin")    
def update_user_profile(request):
    if request.method == 'POST':
        if isinstance(request.user, ScoutUser):
            user = ScoutUser.objects.get(userid = request.user.userid)
            tryForm = ScoutUserProfileForm(request.POST, instance=user)

            if tryForm.is_valid():
                updatedForm = tryForm.save(commit=False)
                updatedForm.save()
                #success(request, 'Your profile has been updated')
                return redirect('user_profile')
            else:
                #error(request, 'Form is invalid')
                return redirect('user_profile')
        
    elif isinstance(request.user, ScoutUser_Landlord):
        user = ScoutUser_Landlord.objects.get(userid = request.user.userid)
        tryForm = LandlordUserProfileForm(  request.POST, instance=user)

        if tryForm.is_valid():
            updatedForm = tryForm.save(commit=False)
            updatedForm.save()
            #success(request, 'Your profile has been updated')
            return redirect('user_profile')
        else:
            print(tryForm.errors)
            #error(request, 'Form is invalid')
            return redirect('user_profile')
                        
def go_map(request):

    context = {}
    return render(request, 'RentScout/map.html', context)

@login_required(login_url = "signin")
def all_reports(request):
    context = {}
    return render(request, 'RentScout/admin/all_reports.html', context)

@login_required(login_url = "signin")
def all_verification(request):
    context = {}
    return render(request, 'RentScout/admin/verification.html', context)

@login_required(login_url = "signin")
def bookmark_page(request):
    return render(request, 'RentScout/bookmarks.html', {})

class get_all_reports(View):
    def get(self, request):
        page = request.GET.get('page', 1)
        try:
            reports_all = BuildingReport.objects.all()
            paginator = Paginator(reports_all, 10)
            report_page = paginator.get_page(page)
            report_datas = [
                {
                'reportid': report.reportid,
                'buildingid': report.buildingid.buildingid,
                'building_image': report.buildingid.building_image.url,
                'building_name': report.buildingid.building_name,
                'reporter': report.reporter.email,
                'date_reported': report.date_reported,
                'reason': report.reason
                }
                for report in report_page
            ]

            response_data = {
                'reports': report_datas,
                'total_pages': paginator.num_pages,
                'current_page': report_page.number,
                'has_next': report_page.has_next(),
                'has_previous': report_page.has_previous(),
            }
            return JsonResponse(response_data, status = 200)
        except BuildingReport.DoesNotExist:
            return JsonResponse({'error': "Building Reports Does Not Exist"}, status = 404)
        except Exception as e:
            return JsonResponse({'error': f'{e}'})

class get_buildings_bypage(View):
    def get(self, request):
        page = request.GET.get('page', 1)

        filter = request.GET.get('filter', None)

        if filter == '':
            filter = None

        if not page:
            return JsonResponse({'error': 'Did not recieve Building ID'}, status = 405)
        
        try:
            if filter is not None:
                try:
                    filter_numeric = int(filter)
                except ValueError:
                    filter_numeric = None

                all_buildings = Building.objects.filter(
                    Q(building_name__icontains = filter) |
                    Q(street__icontains = filter) |
                    Q(city__icontains = filter) |
                    Q(province__icontains = filter) |
                    Q(country__icontains = filter) |
                    Q(coordinates__icontains = filter) |
                    (Q(zip_code = filter_numeric) if filter_numeric is not None else Q()) |
                    (Q(average_rating = filter_numeric) if filter_numeric is not None else Q())
                )
            else:
                all_buildings = Building.objects.all()
            
            paginator = Paginator(all_buildings, 8)

            building_page = paginator.get_page(page)
            user_bookmarks = []

            if isinstance(request.user, ScoutUser):
                current_user = request.user
                user_bookmarks = ScoutUserBookmark.objects.filter(owner=current_user).values_list('buildingid', flat=True)
                print(f'user is scout: {current_user.email}')
            elif isinstance(request.user, ScoutUser_Landlord):
                current_user = request.user
                user_bookmarks = LandlordUserBookmark.objects.filter(owner=current_user).values_list('buildingid', flat=True)
                print(f'user is landlord: {current_user.email}')
            elif isinstance(request.user, AdminUser):
                current_user = request.user
                print(f'user is admin: {current_user.email}')
            else:
                current_user = None
                print('User type is not recognized.')


            building_data = [
                {
                    'building_id': building.buildingid,
                    'building_name': building.building_name,
                    'building_address': building.complete_address(),
                    'building_image': building.building_image.url if building.building_image else None,
                    'bookmark_status': building.buildingid in user_bookmarks    
                }   
                for building in building_page
            ]
            response_data = {
                'building_datas': building_data,
                'total_pages': paginator.num_pages,
                'current_page': building_page.number,
                'has_next': building_page.has_next(),
                'has_previous': building_page.has_previous(),
            }

            return JsonResponse(response_data)
        
        except Building.DoesNotExist:
            return JsonResponse({'error': "Buildings Does Not Exist"}, status = 404)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status = 500)

class create_room_view(View):
    def post(self, request):
        buildingid = request.POST.get('buildingid')
        
        if not buildingid:
            return JsonResponse({'error': 'Requires Building ID'}, status = 400)
        
        try:
            building = Building.objects.get(buildingid = buildingid)
            room_form = RoomForm(request.POST)
            print(room_form)
            if room_form.is_valid():
                new_room = room_form.save(commit=False)
                new_room.building_id = building
                new_room.save()
                return JsonResponse({'success': 'New room created'}, status=200)
            else:
                print(room_form.errors)
                return JsonResponse({'error': 'Form is invalid'}, status = 400)
        except Building.DoesNotExist:
            return JsonResponse({'error': 'Buildings Does Not Exist'}, status = 404)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status = 500)

class get_rooms(View):
    def get(self,request):
        query = request.GET.get('building_id', '')
        print(query)
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
                #error(request, 'Error 404: Rooms Not Found')
                JsonResponse({'error': 'Rooms Not Found'}, status=404)
            except Exception as e:
                JsonResponse({'error': f'{e}'}, status = 500)

        else:
            #error(request, 'Error 405: Bad request')
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
                    'priv_bathroom': room.priv_bathroom,
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

class update_room(View):
    def post(self, request):
        room_id = request.POST.get('room_id', '')
        if room_id:
            try:
                room = Room.objects.get(roomid = room_id)
                roomForm = RoomForm(request.POST, instance=room)
                if roomForm.is_valid():
                    roomForm.save()
                    return JsonResponse({'success': 'successfully updated Room'}, status = 200)
                else:
                    return JsonResponse({'error': 'Form invalid'}, status = 400)
            except Room.DoesNotExist:
                return JsonResponse({'error': 'Room Does Not Exist'}, status = 404)
            except Exception as e:
                return JsonResponse({'error': e}, status = 500)
        else:
            return JsonResponse({'error': 'Did not receive Room ID'}, status = 400)

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
                return JsonResponse({'error': e}, status = 500)
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

class get_policies(View):
    def get(self, request):
        bldg_id = request.GET.get('building_id', '')
        if bldg_id:
            try:
                policies = Policies.objects.filter(buildingid = bldg_id)
                print(policies)
                policy_list = []
                for policy in policies:
                    policy_list.append({
                        'policy_id': policy.policy_id,
                        'policy': policy.policy
                    })
                response_data = {
                    'policy_lists': policy_list
                }
                return JsonResponse(response_data)
            except Exception as e:
                return JsonResponse({'error': f"{e}"}, status = 500)
        else:
            return JsonResponse({'error': 'Did not receive Building ID'}, status = 400)

# create new policy
class save_policy_view(View):
    def post(self, request):
        query = request.POST.get('buildingid')
        if query:
            try:
                building = Building.objects.get(buildingid = query)
                form = PoliciesForm(request.POST)
                if form.is_valid():
                    new_pol = form.save(commit=False)
                    new_pol.buildingid = building
                    new_pol.save()
                    return JsonResponse({'success': "New Policy Saved"}, status = 200)
            except Building.DoesNotExist:
                return JsonResponse({'error': 'Building Does Not Exist'}, status = 404)
            except Exception as e:
                return JsonResponse({'error': f'{e}'}, status = 500)
        else:
            return JsonResponse({'error': "Did not receive Building ID"}, status = 400)

class del_policy_view(View):
    def post(self, request):
        policy_id = request.POST.get('policy_id')
        if policy_id:
            policy = Policies.objects.get(policy_id = policy_id)
            policy.delete()
            return JsonResponse({'success': 'Policy Deleted'},status=200)
        else:
            return JsonResponse({'error': f"Policy({policy_id}) does not Exist"}, status=400)

class update_policy_view(View):
    def post(self, request):
        policy_id = request.POST.get('policy_id')
        if policy_id:
            # print(policy_id)
            try:
                policy = Policies.objects.get(policy_id = policy_id)
                old_policy = PoliciesForm(request.POST, instance = policy)
                # print(request.POST)
                print(old_policy)
                if old_policy.is_valid():
                    old_policy.save(commit=False)
                    old_policy.save()
                    print('UPdate policy success')
                    return JsonResponse({'success': "successfully updated policy"}, status = 200)
                else:
                    print(old_policy.errors)
                    return JsonResponse({'error': 'Policy form is invalid'}, status = 400)
            except Policies.DoesNotExist:
                return JsonResponse({'error': 'Policy does not exist'}, status = 404)
            except Exception as e:
                return JsonResponse({'error': f'{e}'}, status = 500)
        else:
            return JsonResponse({'error': 'Did not recieve Policy ID'}, status = 400)

class create_amenity_view(View):
    def post(self, request):
        building_id = request.POST.get('building_id')
        building = Building.objects.get(buildingid = building_id)
        print(request.POST)
        if building_id:
            try:
                form = HighlightsForm(request.POST)
                if form.is_valid():
                    newamenity = form.save(commit=False)
                    newamenity.buildingid = building
                    newamenity.save()
                    return JsonResponse({'success': 'successfully created amenity'}, status = 200)
                else:
                    print(form.errors)
                    return JsonResponse({'error': 'Form data invalid'}, status=400)
            except:
                return JsonResponse({'error': 'Failed to create form'}, status = 500)
        else:
            return JsonResponse({'error': 'Did not get Building ID'}, status = 400)
        
class request_amenity_status(View):
    def get(self, request):
        building_id = request.GET.get('building_id', '')
        print(building_id)
        if building_id:
            try:
                print("has building id", building_id)
                amenity = Highlights.objects.get(buildingid = building_id)
                # amenity_form = HighlightsForm(instance = amenity)
                print(building_id)
                response_data = {
                    'status': 200,
                    'building_name': amenity.buildingid.building_name,
                    'free_wifi': amenity.free_wifi,
                    'shared_kitchen': amenity.shared_kitchen,
                    'smoke_free': amenity.smoke_free,
                    'janitor': amenity.janitor,
                    'guard': amenity.guard,
                    'waterbill': amenity.waterbill,
                    'electricbill': amenity.electricbill,
                    'food': amenity.food
                    # 'amenity_form': amenity_form
                }
                return JsonResponse(response_data, safe = False, status = 200)
            except Highlights.DoesNotExist:
                response_data = {
                    'error': "Highlights does not exist",
                    'status': 404,
                }
                return JsonResponse(response_data, safe = False, status=200)
                # return JsonResponse({'error': 'Highlights does not exist'}, status = 404)
            except Exception as e:
                return JsonResponse({'form_html': f'{e}'}, status=500)        
        else:
            return JsonResponse({'error': 'Did not get Building ID'}, status = 400)

class update_amenity_view(View):
    def post(self, request):
        building_id = request.POST.get('building_id')
        print(building_id)
        if building_id:
            try:
                building = Building.objects.get(buildingid = building_id)
                amenity = Highlights.objects.get(buildingid = building)
                amenityForm = HighlightsForm(request.POST, instance=amenity)
                if amenityForm.is_valid():
                    amenityForm.save(commit=False)
                    amenityForm.save()
                    return JsonResponse({'success': 'successfully update Amenity'}, status =200)
                else:
                    return JsonResponse({'error': 'Form invalid'}, status = 400)
            except Highlights.DoesNotExist:
                return JsonResponse({'error': 'Amenity not found'}, status = 404)
            except Exception as e:
                return JsonResponse({'error': f'CLement {e}'}, status = 500)
        else:
            return JsonResponse({'error': 'Did not recieve Building ID'}, status = 400)
                
class get_bookmark_status(View):
    def get(self, request):
        building_id = request.GET.get('buildingid', '')
        if building_id:
            try:
                print('has building id')
                if isinstance(request.user, ScoutUser): 
                    print('an instance of scoutuser')
                    user = ScoutUser.objects.get(userid = request.user.userid)
                    building = Building.objects.get(buildingid = building_id)
                    bookmark = ScoutUserBookmark.objects.filter(owner=user, buildingid=building)
                    print(bookmark)
                    if bookmark:
                        return JsonResponse({'success': 'Already Bookmarked',
                                             'buildingid': building_id}, status = 200)
                    else:
                        return JsonResponse({'success': 'Not Bookmarked',
                                             'buildingid': building_id}, status = 200)
                    
                elif isinstance(request.user, ScoutUser_Landlord):  
                    print('an instance of landlord')
                    user = ScoutUser_Landlord.objects.get(userid = request.user.userid)
                    building = Building.objects.get(buildingid = building_id)
                    bookmark = LandlordUserBookmark.objects.filter(owner=user, buildingid=building)
                    print(bookmark)
                    if bookmark:
                        return JsonResponse({'success': 'Already Bookmarked',
                                             'buildingid': building_id}, status = 200)
                    else:
                        return JsonResponse({'success': 'Not Bookmarked',
                                             'buildingid': building_id}, status = 200)
                
                elif isinstance(request.user, AdminUser):
                    return JsonResponse({'success': 'Not Bookmarked',
                                            'buildingid': building_id}, status = 200)
                
                else:
                    return JsonResponse({'error': 'User is not a true user'}, status = 500)
                
            except Building.DoesNotExist:
                return JsonResponse ({'error': 'Buildingdoes not exist'}, status = 500)
            except Exception as e:
                return JsonResponse({'error': f'{e}'}, status = 500)
        else:
            return JsonResponse({'error': 'Did not get Building ID'}, status = 405)

class get_bookmark_all(View):
    def get(self, request):
        page = request.GET.get('page', 1)
        filter = request.GET.get('query', None)
        if filter == '':
            filter = None

        if not page:
            return JsonResponse({'error': 'Page Not Found'}, status = 404)
        
        try:
            if isinstance(request.user, ScoutUser):
                user = ScoutUser.objects.get(userid = request.user.userid)

                if filter == None:
                    bookmarks = ScoutUserBookmark.objects.filter(owner = user)
                else:
                    try:
                        filter_numeric = int(filter)
                    except ValueError: 
                        filter_numeric = None

                        bookmarks = ScoutUserBookmark.objects.filter(
                            Q(buildingid__building_name__icontains = filter) |
                            (Q(buildingid__zip_code = filter_numeric) if filter_numeric is not None else Q()) |
                            Q(buildingid__street__icontains = filter) |
                            Q(buildingid__city__icontains = filter) |
                            Q(buildingid__province__icontains = filter) |
                            Q(buildingid__country__icontains = filter) |
                            Q(owner__email__icontains = filter) |
                            Q(owner__firstname__icontains = filter) |
                            Q(owner__lastname__icontains = filter) |
                            Q(owner__middlename__icontains = filter),
                            owner = user
                        )
                        print(bookmarks)

            elif isinstance(request.user, ScoutUser_Landlord):
                user = ScoutUser_Landlord.objects.get(userid = request.user.userid)
                if filter == None:
                    bookmarks = LandlordUserBookmark.objects.filter(owner = user)
                else:
                    try:
                        filter_numeric = int(filter)
                    except ValueError: 
                        filter_numeric = None

                        bookmarks = LandlordUserBookmark.objects.filter(
                            Q(buildingid__building_name__icontains = filter) |
                            (Q(buildingid__zip_code = filter_numeric) if filter_numeric is not None else Q()) |
                            Q(buildingid__street__icontains = filter) |
                            Q(buildingid__city__icontains = filter) |
                            Q(buildingid__province__icontains = filter) |
                            Q(buildingid__country__icontains = filter) |
                            Q(owner__email__icontains = filter) |
                            Q(owner__firstname__icontains = filter) |
                            Q(owner__lastname__icontains = filter) |
                            Q(owner__middlename__icontains = filter),
                            owner = user
                        )
            elif isinstance(request.user, AdminUser):
                return JsonResponse({'error': 'Admin Users cannot Bookmark'}, status = 400)
            else:
                return JsonResponse({'error': 'You need to Log in'}, status = 400)
            
            paginator = Paginator(bookmarks, 10)
            current_page = paginator.get_page(page)
            bookmark_data = [
                {
                    'building_id': building.buildingid.buildingid,
                    'building_name': building.buildingid.building_name,
                    'building_address': building.buildingid.complete_address(),
                    'building_image': building.buildingid.building_image.url if building.buildingid.building_image else None 
                }
                for building in current_page
            ]

            response_data = {
                'bookmarks': bookmark_data,
                'total_pages': paginator.num_pages,
                'current_page': current_page.number,
                'has_next': current_page.has_next(),
                'has_previous': current_page.has_previous(),
            }
            
            print(response_data)

            return JsonResponse(response_data, status = 200)
        except ScoutUserBookmark.DoesNotExist:
            return JsonResponse({'error': 'Scout Users Bookmarks Not Found'})
        except LandlordUserBookmark.DoesNotExist:
            return JsonResponse({'error': 'Landlord Users Bookmarks Not Found'}, status = 404)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status = 500)

class create_bookmark(View):
    def post(self, request):
        if isinstance(request.user, ScoutUser):
            form = ScoutBookmarkForm(request.POST)
            if form.is_valid():
                newbookmark = form.save(commit=False)
                newbookmark.owner = request.user
                newbookmark.save()
                return JsonResponse({'success': 'Saved to Bookmark'}, status = 200)
            else:
                return JsonResponse({'error': 'Form invalid'}, status = 400)
            
        elif isinstance(request.user, ScoutUser_Landlord):
            form = LandlordBookmarkForm(request.POST)
            if form.is_valid():
                newbookmark = form.save(commit=False)
                newbookmark.owner = request.user
                newbookmark.save()
                return JsonResponse({'success': 'Saved to Bookmark'}, status = 200)
            else:
                return JsonResponse({'error': 'Form invalid'}, status = 400)
            
        else:
            #error(request, "Admin Users cannot make bookmarks")
            return JsonResponse({'error': 'Admin Users cannot make bookmarks'}, status = 400)

class remove_bookmark(View):
    def post(self, request):
        buildingid = request.POST.get('building_id')
        if buildingid is None:
            return JsonResponse({'error': 'Did not receive Building ID'})
        
        if isinstance(request.user, ScoutUser):
            building = Building.objects.get(buildingid= buildingid)
            user = ScoutUser.objects.get(userid = request.user.userid)
            bookmark = ScoutUserBookmark.objects.filter( owner=user, buildingid = building )
            bookmark.delete()
            return JsonResponse({'success': 'Bookmark has been removed'}, status = 200)
        elif isinstance(request.user, ScoutUser_Landlord):
            building = Building.objects.get(buildingid= buildingid)
            user = ScoutUser_Landlord.objects.get(userid = request.user.userid)
            bookmark = LandlordUserBookmark.objects.filter( owner=user, buildingid = building )
            bookmark.delete()
            return JsonResponse({'success': 'Bookmark has been removed'}, status = 200)

class create_building_report(View):
    def post(self, request):
        print('posting')
        try:
            buildingid = request.POST.get('buildingid')
            print(buildingid)
            user = ScoutUser.objects.get(userid = request.user.userid)
            building = Building.objects.get(buildingid = buildingid)

            form = BuildingReportForm(request.POST)
            print(request.POST)
            if form.is_valid():
                
                new_report = form.save(commit=False)
                new_report.buildingid = building
                new_report.reporter = user
                new_report.save()
                print(new_report)
                #success(request, "Report successfully sent")
                return JsonResponse({'success': 'Thank you for your report. Our team will review the issue and take appropriate action'}, status = 200)
            else:
                print(form.errors)
                #error(request, 'Report Invalid')
                return JsonResponse({'error': 'Please provide a reason for your report'}, status = 405)
        except ScoutUser.DoesNotExist:
            return JsonResponse({'error': 'User Does Not Exist'}, status = 404)
        except Building.DoesNotExist:
            return JsonResponse({'error': 'Building Does Not Exist'}, status = 404)
        except Exception as e:
            return JsonResponse({'error': "Form Not Allowed"}, status = 500)

class delete_building_report(View):
    def post(self, request):
        reportid = request.POST.get('reportid')
        print(reportid)
        if not reportid:
            return JsonResponse({'error': 'Did not receive Report ID'}, status = 400)
        
        try:
            report = BuildingReport.objects.get(reportid = reportid)
            report.delete()
            #success(request, 'Report successfully Denied')
            return JsonResponse({'success': 'Report successfully Denied'}, status = 200)
        except BuildingReport.DoesNotExist:
            return JsonResponse({'error': 'Report Does Not Exist'}, status = 404)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status = 500)
    

# GETS ALL VERIFICATIONS FOR ADMIN
class get_verification_requests(View):
    def get(self, request):
        page = request.GET.get('page', 1)
        try:
            verification_requests = Verification.objects.filter(status = 'Pending')
            paginator = Paginator(verification_requests, 10)
            current_page = paginator.get_page(page)
            verificaton_datas = [
                {
                'verificationid': verification.verificationid,
                'buildingid': verification.buildingid.buildingid,
                'building_name': verification.buildingid.building_name,
                'building_owner_email': verification.buildingid.building_owner.email,
                'building_owner_id': verification.buildingid.building_owner.userid,
                'building_coordinates': verification.buildingid.coordinates,
                'building_description': verification.buildingid.details,
                'date_requested': verification.date_requested,
                'building_image': verification.buildingid.building_image.url
                }
                for verification in current_page
            ]
            response_data = {
                'verification_requests': verificaton_datas,
                'total_pages': paginator.num_pages,
                'current_page': current_page.number,
                'has_next': current_page.has_next(),
                'has_previous': current_page.has_previous(),
            }
            
            return JsonResponse(response_data, status = 200)
        except Verification.DoesNotExist:
            return JsonResponse({'error': "Verification Does Not Exist"}, status = 404)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status = 500)


# GET VERIFICATION STATUS FOR BUILDING 
class get_verification_status_view(View):
    def get(self, request):
        
        buildingid = request.GET.get('buildingid', '')
        
        if not buildingid:
            return JsonResponse({"error": "Did not receive Building ID"}, status = 400)

        building = Building.objects.get(buildingid = buildingid)

        try:        
            verify = Verification.objects.get(buildingid = building)
            verified_status = verify.status
        except:
            verified_status = 'Not Verified'
        
        return JsonResponse({'verification_status': verified_status}, status = 200)

class create_verification_view(View):
    def post(self, request):

        buildingid = request.POST.get('buildingid')
        if not buildingid:
            return JsonResponse({"error": "Did not receive Building ID"}, status = 400)
        
        building = Building.objects.get(buildingid = buildingid)
        # CHECK IF LOGGED IN USER IS OWNER
        if not building.building_owner == request.user:
            return JsonResponse({"error": "Must be the owner of this building to request verification"}, status = 400)

        try:
            form = VerificationForm(request.POST)
            if form.is_valid():
                new_verification = form.save(commit = False)
                new_verification.status = 'Pending'
                new_verification.save()
                #success(request, 'Verification request has been sent')
                return JsonResponse({'success': 'Verification request has been sent'}, status = 200)
            else:
                return JsonResponse({'error': 'Something went wrong with the form'}, status = 400)
        except Exception as e:
            #error(request, "Server Error")
            return JsonResponse({'error': f'{e}'}, status = 500)

class delete_verification(View):
    def post(self, request):
        buildingid = request.POST.get('buildingid')
        if not buildingid:
            return JsonResponse({"error": "Did not receive Building ID"}, status = 400)
        try:
            # user = ScoutUser_Landlord.objects.get(userid = request.user.userid)
            building = Building.objects.get(buildingid = buildingid)
            verification = Verification.objects.get(buildingid = building)
            verification.delete()
            #success(request, 'Verification request removed')
            return JsonResponse({'success': 'Verification request removed'}, status = 200)
        except Building.DoesNotExist:
            return JsonResponse({'error': 'Building Does Not Exist'}, status = 404)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status = 500)

# GET BUILDING INFO FOR DENY

class deny_verification(View):
    def get(self, request):
        verificationid = request.GET.get('verificationid')
        if not verificationid:
            return JsonResponse({'error': 'Did not receive Verification ID'}, status = 400)
        
        try:
            verification = Verification.objects.get(verificationid = verificationid)
            
            response_data = {
                'building_name': verification.buildingid.building_name,
                'building_owner': verification.buildingid.building_owner.email,
            }
            print('success')
            return JsonResponse(response_data, status = 200)
        except Verification.DoesNotExist:
            return JsonResponse({'error': 'Building Does Not Exist'}, status = 404)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status = 500)
    
    def post(self, request):
        verificationid = request.POST.get('verificationid')
        if not verificationid:
            return JsonResponse({"error": "Did not receive Building ID"}, status = 400)

        try:
            verification = Verification.objects.get(verificationid = verificationid)
            verification.delete()
            #success(request, 'Verification request removed')
            return JsonResponse({'success': 'Verification request removed'}, status = 200)
        
        except Verification.DoesNotExist:
            return JsonResponse({'error': 'Verification Does Not Exist'}, status = 404)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status = 500)

class accept_verification(View):
    def post(self, request):
        verificationid = request.POST.get('verificationid')
        if not verificationid:
            return JsonResponse({"error": "Did not receive Building ID"}, status = 400)

        try:
            verification = Verification.objects.get(verificationid = verificationid)
            verification.status = 'Verified'
            verification.save()
            #success(request, 'Verification accepted')
            return JsonResponse({'success': 'Verification accepted'}, status = 200)
        except Verification.DoesNotExist:
            return JsonResponse({'error': 'Verification Does Not Exist'}, status = 404)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status = 500)


# SCRAPPER
def building_file_scrapper(request):
    if request.method == 'POST':
        file = ScrapperFile(request.POST, request.FILES)
        print(request.FILES)
        if file.is_valid():
            csv_file = request.FILES['file']
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            user = ScoutUser_Landlord.objects.get(userid = 1)
            try:
                for row in reader:
                # Prepare the building data
                    form = BuildingForm({
                        'building_name': row.get('building_name', ''),
                        'zip_code': row.get('zip_code', 0),
                        'street': row.get('street', ''),
                        'city': row.get('city', 'None'),
                        'province': row.get('province', 'None'),
                        'country': row.get('country', 'None'),
                        'details': row.get('details', ''),
                        'rooms_vacant': row.get('rooms_vacant', 0),
                        'coordinates': row.get('coordinates', ''),
                        'average_rating': row.get('average_rating', 0.0),
                    })

                    if form.is_valid():
                        newBuilding = form.save(commit=False)
                        newBuilding.building_owner = user
                        newBuilding.building_image = f"/upload/building_imgs/{row.get('building_image')}"
                        newBuilding.save()
                    
            except Exception as e:

                #error(request, f"{e}")
                return redirect('building_scrapper')
        else:
                #error(request, "File Scrapper Invalid")
                print(file.errors)
                return redirect('building_scrapper')
    form = ScrapperFile()
    return render(request, 'RentScout/building_scrapper.html', {"form":form})