from django.shortcuts import render, redirect
from .models import (ScoutUser, Building, Highlights, Room, 
                     RoomImage, Policies, Feedback, ScoutUser_Landlord,
                     ScoutUserBookmark, LandlordUserBookmark, AdminUser, BuildingReport,
                     Verification, Reservation, Certificate, Message, Payment, 
                     CreatedBoarder, UpdatedBoarder, CreatedLandlord, UpdatedLandlord,
                     DeletedBuilding, CreatedBuilding, UpdatedBuilding,
                     CreatedRoom, UpdatedRoom, DeletedRoom,
                     CreatedPayment, AcceptedPayment, DeniedPayment, CreatedReport,
                     CreatedVerification, AcceptedVerification, DeniedVerification,
                     DeletedVerification, AcceptedReport, DeniedReport

                    )

from .forms import (EmailAuthenticationForm, BuildingForm, UserLoginForm, 
                    ScoutUserCreationForm, RoomForm, RoomImageForm, FeedBackForm,
                    LandlordUserCreationForm, PoliciesForm, HighlightsForm,
                    ScoutUserProfileForm, LandlordUserProfileForm,
                    ScoutBookmarkForm, LandlordBookmarkForm, ScrapperFile, BuildingReportForm,
                    VerificationForm, ReservationForm, CertificateForm, PaymentForm,

                    )
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist as ObjException, ValidationError

from django.views import View
from django.db.models import Q, Count, Case, When, Value, IntegerField, OuterRef, Subquery
from django.http import JsonResponse
from django.contrib import messages
from django.template.loader import render_to_string


import logging, math, csv, qrcode, random, string
from django.core.paginator import Paginator
from django.utils import timezone
from django.utils.dateformat import format as datetimeformat
from datetime import datetime, timedelta
from PIL import Image

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


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
    try:
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
                    messages.error(request, 'Please enter a valid email or password') # 
            
            elif role == 'Landlord':
                form = LandlordUserCreationForm(request.POST)

                if form.is_valid():
                    user = form.save()
                    backend = get_user_backend(user)
                    login(request, user, backend)
                    return redirect('home')
                else:
                    messages.error(request, 'Please enter a valid email or password')
            else:
                messages.error(request, "Please select user type")
    except Exception as e:
        print(e)
        messages.error(request, "Server side error")

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
    qr_code = building.gcash_qr.url if building.gcash_qr else ''

    try:
        verification = Verification.objects.get(buildingid = building)
        verification_status = verification.status
    except Exception as e:
        pass

    context = {'building':building, 'highlights': highlights, 'room_images': room_images,
               'rooms':rooms, 'policies':policies, 'roomform':roomform, 'feedbacks':feedbacks,
               'feedbackform':feedbackForm, 'building_report_form': reportform, 
               'verification': verification_status, 'qr_code': qr_code,
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
        certificate_form = CertificateForm()
    except ObjException as e:
        messages.error(request, f'{e}')

    context = {'buildings':buildings, 'photoform': photo_form, 'amenities_form':amenities_form,
               'bldg_form': building_form, 'certificate_form': certificate_form
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
            messages.success(request, f'Building {newbuilding.building_name} has been created')
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
                form_data['building_image'] = building.building_image.url if building.building_image else '/media/upload/building_imgs/no-image.png'
                form_data['gcash_qr'] = building.gcash_qr.url if building.gcash_qr else '/media/upload/building_imgs/gcash/no-image.png'
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
                bldg_form = BuildingForm(request.POST, request.FILES, instance = building,)
                print(request.FILES)
                if bldg_form.is_valid():
                    print("bldg form is valid")
                    new_bldg = bldg_form.save(commit = False)

                    if 'building_image' in request.FILES:
                        new_bldg.building_image = request.FILES['building_image']

                    if 'gcash_qr' in request.FILES:
                        new_bldg.gcash_qr = request.FILES['gcash_qr']

                    new_bldg.save()
                    return JsonResponse({'success': f'successfully updated {building.building_name} Building'}, status = 200)
                else:
                    return JsonResponse({"error": 'Form update is invalid'}, status = 500)
            except Building.DoesNotExist:
                return JsonResponse({'error': "Building doesn't exist"}, status = 405)
        else:
            return JsonResponse({'error': "Did not get building id"}, status =405)

class delete_building(View):
    def post(self, request):
        try:
            buildingid = request.POST.get('buildingid')

            if not buildingid:
                return JsonResponse({'error': 'Building Not Found'}, status=400)
            
            building = Building.objects.get(buildingid = buildingid)
            building.delete()
            messages.success(request, f"Building {building.building_name} successfully deleted")
            return JsonResponse({'success': f"Building {building.building_name} successfully deleted"}, status = 200)
        except Exception as e:
            print(e)
            return JsonResponse({'error': 'Internal Server Error'}, status = 500)

class delete_building_view(View): # DELETE A BUILDING THROUGH REPORT
    def post(self, request):
        try:
            buildingid = request.POST.get('buildingid')
            reportid = request.POST.get('reportid')
            print('Received building id:', buildingid)  # Debugging line
            
            if not buildingid:
                return JsonResponse({'error': 'Building ID not provided'}, status=400)

            building = Building.objects.get(buildingid=buildingid)
            report = BuildingReport.objects.get(reportid = reportid)

            AcceptedReport.objects.create(
                reportid=report.reportid,
                building=building.building_name,
                reporter=report.reporter.get_fullname,
                reason=report.reason
            )
            
            building.delete()

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
            messages.error(request, "Feedback is invalid")
            return redirect('building_info', request.POST.get('boardingid'))

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
        if not request.POST.get('userid'):
            messages.error(request, "Form invalid")
            print(request.POST.get('profile_image'))
        if isinstance(request.user, ScoutUser):
            user = ScoutUser.objects.get(userid = request.user.userid)
            tryForm = ScoutUserProfileForm(request.POST, request.FILES, instance=user)

            if tryForm.is_valid():
                updatedForm = tryForm.save(commit=False)
                updatedForm.save()
                messages.success(request, 'Your profile has been updated')
                return redirect('user_profile')
            else:
                messages.error(request, 'Form is invalid')
                return redirect('user_profile')
        
        elif isinstance(request.user, ScoutUser_Landlord):
            user = ScoutUser_Landlord.objects.get(userid = request.user.userid)
            tryForm = LandlordUserProfileForm(  request.POST, request.FILES, instance=user)

            if tryForm.is_valid():
                updatedForm = tryForm.save(commit=False)
                updatedForm.save()
                messages.success(request, 'Your profile has been updated')
                return redirect('user_profile')
            else:
                print(tryForm.errors)
                messages.error(request, 'Form is invalid')
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

@login_required(login_url = "signin")
def reservation_page(request):
    buildings = Building.objects.filter(building_owner = request.user).annotate( 
                                        reservation_count = Count(
                                            Case(
                                                When(room_of_building__reserved_room__status="Pending", then=1),
                                                output_field=IntegerField(),
                                                )
                                            )
                                        )
    
    context = {'buildings':buildings}
    return render(request, 'RentScout/reservations.html', context)

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
                    # 'price': room.price,
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

class delete_room(View):
    def post(selt, request):
        try: 
            roomid = request.POST.get('roomid')

            if not roomid or roomid is None:
                return JsonResponse({'error': 'Room not Found'}, status = 404)
            
            room = Room.objects.get(roomid = roomid)
            room_name = room.room_name
            room.delete()
            return JsonResponse({'success': f'Room "{room_name}" successfully DELETED'}, status = 200)
        
        except Exception as e:
            print(f'{e}')
            return JsonResponse({'error': 'Server Error'}, status = 500)
    
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
            if not roomid:
                messages.error(request, 'Error Room')
                return JsonResponse({'message': 'Error Room'}, status = 404)
            
            photoform = RoomImageForm(request.POST, request.FILES)
            room = Room.objects.get(roomid = roomid)
            if photoform.is_valid():
                print('valid photo form')
                newphoto = photoform.save(commit=False)
                newphoto.roomid = room
                newphoto.save()
                return JsonResponse({'message': 'Photo uploaded'}, status = 200)
            else:
                print(photoform.errors)
                return JsonResponse({'error': 'Error Photo form'}, status = 400)
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
                
class upload_certificate_view(View):
    def post(self, request):
        try:
            buildingid = request.POST.get('buildingid')
            certificate_form = CertificateForm(request.POST, request.FILES)
            building = Building.objects.get(buildingid = buildingid)
            if certificate_form.is_valid():
                print('valid photo form')
                newcertificate = certificate_form.save(commit=False)
                newcertificate.save()
                return JsonResponse({'message': 'Certificate uploaded'}, status = 200)
            else:
                print(certificate_form.errors)
                return JsonResponse({'error': "Form Invalid"}, status = 400)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status = 500)
        
class get_certificates_view(View):
    def get(self, request):
        try:
            buildingid = request.GET.get('buildingid', None)
            if not buildingid or buildingid is None:
                return JsonResponse({'error': "Incomplete Request"}, status = 400)
            
            building = Building.objects.get(buildingid = buildingid)
            certificates = Certificate.objects.filter(buildingid = building, buildingid__building_owner = request.user)
            
            cert_data = [
                {
                    'certificate_id': certificate.certificationid,
                    'certificate_name': certificate.certificate_name,
                }
                for certificate in certificates
            ]
            response_data = {
                'certificates': cert_data
            }
            return JsonResponse(response_data, status = 200)
        
        except Building.DoesNotExist:
            return JsonResponse({'error': "Building Does Not Exist"}, status = 404)
        except Certificate.DoesNotExist:
            return JsonResponse({'error': "Certificate Does Not Exist"}, status = 404)
        except Exception as e:
            return JsonResponse({"error": f"{e}"}, status = 500)

class get_certificate_byid(View):
    def get(self, request):
        try:
            certificate_id = request.GET.get('cert_id', None)
            if not certificate_id or certificate_id is None:
                return JsonResponse({'error': "Incomplete Request"}, status = 400)
            
            certificate = Certificate.objects.get(certificationid = certificate_id)
            
            cert_data = {
                    'image': certificate.image.url if certificate.image else '',
                    'certificate_name': certificate.certificate_name,
                    'date': certificate.date_uploaded.strftime("%B %d, %Y")
                }
            
            return JsonResponse(cert_data, status = 200)
        
        except Building.DoesNotExist:
            return JsonResponse({'error': "Building Does Not Exist"}, status = 404)
        except Certificate.DoesNotExist:
            return JsonResponse({'error': "Certificate Does Not Exist"}, status = 404)
        except Exception as e:
            return JsonResponse({"error": f"{e}"}, status = 500)


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
        try:
            buildingid = request.POST.get('building_id')
            print(buildingid)
            if not buildingid or buildingid is None:
                return JsonResponse({'error': 'Did not receive Building ID'}, status = 405)
            
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
        except:
            return JsonResponse({'error': 'Server Error'}, status = 500)
        
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

            DeniedReport.objects.create(
                reportid=report.reportid,
                building=report.buildingid.building_name,
                reporter=report.reporter.get_fullname,
                reason=report.reason
            )

            report.delete()
            #success(request, 'Report successfully Denied')
            return JsonResponse({'success': 'Report successfully Denied'}, status = 200)
        except BuildingReport.DoesNotExist:
            return JsonResponse({'error': 'Report Does Not Exist'}, status = 404)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status = 500)
    
# class create_boarder_notification(View):
#     def post(self, request):
        



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
                'building_image': verification.buildingid.building_image.url if verification.buildingid.building_image else ''
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

#   RESERVATIONS
class create_reservation(View):
    def post(self, request):
        try:
            roomid = request.POST.get('roomid')
            if not roomid:
                messages.error(request, "Error Room")
                return JsonResponse({"error": "Did not receive Room ID"}, status = 400)

            if isinstance(request.user, ScoutUser):
                form = ReservationForm(request.POST)
                if form.is_valid(): 
                    new_reservation = form.save(commit=False)
                    new_reservation.userid = request.user
                    new_reservation.save()
                    return JsonResponse({'success': "Reservation has been made"}, status = 200)
            else:
                messages.error(request, "This user doesn't have permission to make a reservation")
                return JsonResponse({'error': "User doesn't have permission to make reservation"}, status = 400)
        except Exception as e:
            messages.error(request, "Something went wrong with the server")
            return JsonResponse({'error': f"{e}"})

# GET STATUS OF RESERVATION (FOR BOARDER)        
class get_reservation_instance(View):
    def get(self, request):
        try:
            roomid = request.GET.get('roomid', None)
            print(roomid)
            if not roomid or roomid is None:
                messages.error(request, "Error Room reservation instance")
                return JsonResponse({"error": "Did not receive Room ID"}, status = 400)
            
            room = Room.objects.get(roomid = roomid)

            reservation = Reservation.objects.filter(
                Q(status = "Pending") | 
                Q(status = "Accepted"),
                roomid = room,
                userid = request.user,
            ).order_by(
                Case(
                    When(status="Accepted", then=Value(1)),
                    When(status="Pending", then=Value(2)),
                    default=Value(3),
                    output_field=IntegerField(),
                )
            )
            
            print(reservation)
            
            first_reservation = reservation.first()
            
            if reservation.exists():
                response_data = {
                    'success': bool(first_reservation),
                    'status': first_reservation.status
                }
                return JsonResponse(response_data, status = 200)
            else:
                response_data = {
                    'success': 'False',
                }
                print(response_data)
                return JsonResponse(response_data, status = 200)
        
        except ObjException:
            return JsonResponse({'success': 'False'}, status = 200)
        except Reservation.MultipleObjectsReturned:
            print("Multiple reservations found: Expected only one.")
            return JsonResponse({'success': 'True'}, status = 200)
        except Exception:
            return JsonResponse({'success': "False"}, status = 200)


# GET ALL PENDING RESERVATIONS # =============== SAKTO NA DIRI DAPITA
class get_reservations_pending(View):
    def get(self, request):
        try:
            buildingid = request.GET.get('buildingid', None)
            status = request.GET.get('statusQ', 'Pending')
            
            if not status or status is None:
                status = 'Pending'
                
            print(buildingid)
            print(status)

            if not buildingid or buildingid is None:
                building = Building.objects.filter(building_owner = request.user)
                
                if building.count() > 1:
                    return JsonResponse({'success': f"Select Required"}, status = 200)
                else:
                    # if only 1 building exist
                    building = building.first()
                    reservations = Reservation.objects.filter(
                                        roomid__building_id = building, 
                                        status = status
                                    )
                    reservation_record = [
                        {
                        'reservationid': resv.reservationid,
                        'room_name': resv.roomid.room_name,
                        'boarder_name': resv.userid.get_fullname,
                        'boarder_email': resv.userid.email,
                        'boarder_contact': resv.userid.contact,
                        'created': resv.created,
                        }
                            for resv in reservations
                    ]
                    print('result only 1')

            else: # IF THERE IS BUILDINGID FOR FILTER
                building = Building.objects.get(buildingid = buildingid)
                reservations = Reservation.objects.filter(
                                    roomid__building_id = building,
                                    status = status
                                )
                
                reservation_record = [
                    {
                    'reservationid': resv.reservationid,
                    'room_name': resv.roomid.room_name,
                    'boarder_name': resv.userid.get_fullname,
                    'boarder_email': resv.userid.email,
                    'boarder_contact': resv.userid.contact,
                    'created': resv.created.isoformat(),
                    }
                        for resv in reservations
                ]
                print('result many')
            print(reservations)
            response_data = {
                'reservations': reservation_record,
                'reservation_count': len(reservation_record),
            }
            return JsonResponse(response_data, status = 200)
        except Exception as e:
            return JsonResponse({'error': f"{e}"}, status = 500)


class get_reservations_all(View):
    def get(self, request):
        try:
            buildingid = request.GET.get('buildingid')

            if not buildingid or buildingid is None:
                return JsonResponse({'success': 'No Buildings'}, status = 200)
            
            building = Building.objects.get(buildingid = buildingid)
            room = Room.objects.filter(building_id = building)
            reservations = Reservation.objects.filter( roomid__in = room)

            if not reservations:
                return JsonResponse({'success': 'No Reservations'}, status = 200)

            res_list = [
                {
                    'res_id': res.reservationid,
                    'name': res.userid.get_fullname,
                    'email': res.userid.email,
                    'room': res.roomid.room_name,
                    'date': datetimeformat(res.created, "M. j, Y"),
                    'status': res.status
                }
                for res in reservations
            ]
            
            response_data = {
                'reservation_list': res_list,
                'success': 'Success'
            }

            return JsonResponse(response_data, status = 200)
        
        except Exception as e:
            return JsonResponse({'error': "Server Error"}, status = 500)

class accept_reservation(View):
    def post(self, request):
        try:
            reservationid = request.POST.get('reservationid')
            print(reservationid)
            if not reservationid:
                return JsonResponse({"error": "Error Reservation"}, status = 404)
            
            reservation = Reservation.objects.get(reservationid = reservationid)

            roomid = reservation.roomid 

            reserved_list = list(Reservation.objects.filter(
                Q(status = "Accepted"),
                roomid = roomid
            ))
            print(reserved_list)
            reserved_count = reserved_list.count(0)
            
            if reserved_count < reservation.roomid.person_free:
                reservation.status = 'Accepted'
                reservation.save()
                return JsonResponse({'success': "Successfully accepted reservations"}, status = 200)
            else:
                return JsonResponse({'error': "Cannot accept reservation more than the slot available"}, status = 200)
        
        except Reservation.DoesNotExist:
            return JsonResponse({"error": "Reservation Does Not Exist"}, status = 404)
        except Exception as e:
            return JsonResponse({'error': f"{e}"}, status = 500)

class decline_reservation(View):
    def post(self, request):
        try:
            reservationid = request.POST.get('reservationid')
            
            if not reservationid:
                return JsonResponse({'error': "Error Reservation"}, status = 404)
            
            reservation = Reservation.objects.get(reservationid = reservationid)
            reservation.status = 'Declined'
            reservation.save()
            
            return JsonResponse({'success': 'Reservation Successfuly Declined'}, status = 200)
        
        except Exception as e:
            return JsonResponse({"error": f"{e}"}, status = 500)

class delete_reservation(View): # DELETE RESERVATION BY ROOMID
    def post(self, request):
        try:
            roomid = request.POST.get('roomid')
            if not roomid:
                messages.error(request, "Error Reservation ID")
                return JsonResponse({"error": "Did not receive Building ID"}, status = 400)

            reservation = Reservation.objects.filter(roomid = roomid, userid = request.user)
            reservation.delete() 
            return JsonResponse({'success': "Reservation Canceled"}, status = 200)
        
        except Reservation.DoesNotExist:
            return JsonResponse({'error': "Reservation does not exist"}, status = 404)
        except Exception as e:
            return JsonResponse({'error': f"{e}"}, status = 500)

class delete_reservation_byid(View):
    def post(self, request):
        try:
            reservationid = request.POST.get('reservationid')
            if not reservationid:
                return JsonResponse({"error": "Error Reservation"}, status = 404)
            
            reservation = Reservation.objects.get(reservationid = reservationid)
            reservation.delete()

            return JsonResponse({'success': "Successfully deleted reservation"}, status = 200)
        
        except Reservation.DoesNotExist:
            return JsonResponse({"error": "Reservation Does Not Exist"}, status = 404)
        except Exception as e:
            return JsonResponse({'error': f"{e}"}, status = 500)

latest_message = Message.objects.filter(
    boarder=OuterRef('boarder'),
    landlord=OuterRef('landlord')
).order_by('-date_created')


class get_inbox(View):
    def get(self, request):
        if isinstance(request.user, AdminUser):
            return JsonResponse({'success': 'User is admin'}, status = 200)

        try:
            page = request.GET.get('page', 1)

            # if isinstance(request.user, ScoutUser):
            #     messages = Message.objects.filter(boarder = request.user)
                
            # elif isinstance(request.user, ScoutUser_Landlord):
            #     messages = Message.objects.filter(landlord = request.user)

            if isinstance(request.user, ScoutUser):
                messages = Message.objects.filter(
                    boarder=request.user,
                    messageid=Subquery(latest_message.values('messageid')[:1])
                )
                
            elif isinstance(request.user, ScoutUser_Landlord):
                print('landlorduser')
                messages = Message.objects.filter(
                    landlord=request.user,
                    messageid=Subquery(latest_message.values('messageid')[:1])
                )

            paginator = Paginator(messages, 8)

            # if page is None:
            #     page = paginator.num_pages

            current_page = paginator.get_page(page)

            inboxes = [
                {
                    'receiver_id': inbox.landlord.userid
                        if request.user.usertype == 'Boarder'
                        else inbox.boarder.userid,

                    'user_profile': inbox.landlord.profile_image.url
                        if request.user.usertype == 'Boarder'
                        else inbox.boarder.profile_image.url,

                    'receiver_name': inbox.landlord.get_fullname
                        if request.user.usertype == 'Boarder'
                        else inbox.boarder.get_fullname,

                    'last_message': truncate_message(inbox.message, 40),

                    'sender': inbox.sender,

                    'me': request.user.usertype
                }
                for inbox in current_page
            ]

            print(inboxes)
            response_data = {
                'inbox_list': inboxes,
            }
            return JsonResponse(response_data, status = 200)
        except Exception as e:
            return JsonResponse({'error': f'{e}'}, status = 500)

class get_messages(View):
    def get(self, request):
        try:
            receiverid = request.GET.get('receiverid', None)
            page = request.GET.get('page', None)
            print('unedited_page:', receiverid)

            messages = ''
            if not receiverid or receiverid is None:
                return JsonResponse({'error': "Incomplete Request"}, status = 400)
            
            if isinstance(request.user, ScoutUser):
                receiver = ScoutUser_Landlord.objects.get(userid = receiverid)
                messages = Message.objects.filter(boarder = request.user, landlord = receiver).order_by('-date_created')
                boarder_profile = request.user.profile_image.url if request.user.profile_image else '/media/upload/user_profiles/user.png'
                print("User is Boarder")
                print(boarder_profile)
                landlord_profile = receiver.profile_image.url if receiver.profile_image else '/media/upload/user_profiles/user.png'

            elif isinstance(request.user, ScoutUser_Landlord):
                receiver = ScoutUser.objects.get(userid = receiverid)
                messages = Message.objects.filter(boarder = receiver, landlord = request.user).order_by('-date_created')
                boarder_profile = receiver.profile_image.url if receiver.profile_image else '/media/upload/user_profiles/user.png'
                landlord_profile = request.user.profile_image.url if request.user.profile_image else '/media/upload/user_profiles/user.png'
                
            # PAGINATOR
            paginator = Paginator(messages, 10)

            if not page or page is None:
                page = 1 # paginator.num_pages

            print('page:', page)
            load_page = paginator.get_page(page)
            print(load_page)

            print(boarder_profile)
            print(landlord_profile)
            message_list = [
                {
                    'sender': message.sender,
                    'message': message.message,
                    'time_sent': (# MESSAGE DATE TIME FORMAT
                        message.date_created.strftime('%H:%M')
                        if timezone.now() - message.date_created < timedelta(days=1)
                        else message.date_created.strftime('%A %H:%M')
                        if timezone.now() - message.date_created < timedelta(weeks=1)
                        else message.date_created.strftime('%Y-%m-%d %H:%M')
                    ),
                    'image': message.image.url if message.image and message.image.url else None
                }
                for message in load_page
            ]
            print("messagelist", message_list)

            response_data = {
                'message_list': message_list,
                'has_next': load_page.has_next(),
                'next_page': load_page.number + 1,
                'boarder_profile': boarder_profile,
                'landlord_profile': landlord_profile
            }
            
            return JsonResponse(response_data, status = 200)

        except Exception as e:
            return JsonResponse({'error': f"{e}"}, status = 500)

class request_building_userid(View): # GET USERID FROM BUILDING
    def get(self, request):
        try:
            buildingid = request.GET.get('buildingid')
            if not buildingid:
                return JsonResponse({'error': 'Incomplete Request'}, status = 400)
            
            building = Building.objects.get(buildingid = buildingid)
            response_data = {
                'success': building.building_owner.userid,
                'profile_image': building.building_owner.profile_image.url,
                'receiver_name': building.building_owner.get_fullname
            }
            return JsonResponse(response_data, status = 200)
        except Exception as e:
            return JsonResponse({'error': f"{e}"}, status = 500)
        
class request_userid(View):
    def get(self, request):
        try:
            receiverid = request.GET.get('receiver_id', None)
            if not receiverid or receiverid is None:
                return JsonResponse({'error': 'Incomplete Request'}, status = 400)
            
            if isinstance(request.user, ScoutUser):
                user = ScoutUser_Landlord.objects.get(userid = receiverid)

            elif isinstance(request.user, ScoutUser_Landlord):
                user = ScoutUser.objects.get(userid = receiverid)

            response_data = {
                'success': user.userid,
                'profile_image': user.profile_image.url,
                'receiver_name': user.get_fullname
            }
            return JsonResponse(response_data, status = 200)
        except Exception as e:
            return JsonResponse({'error': f"{e}"}, status = 500)
        
# CREATE MESSAGE VIA BOARDING HOUSE PAGE
class create_message(View):
    def post(self, request):
        try:
            images = request.FILES.getlist('images')
            message = request.POST.get('message')
            receiverid = request.POST.get('receiverid')
            print(images,message,receiverid)

            if (not message and not images) or not receiverid:
                return JsonResponse({'error': 'Empty Messages'}, status = 400)
            
            if isinstance(request.user, ScoutUser):
                landlord = ScoutUser_Landlord.objects.get(userid = receiverid)
                boarder = request.user
                
                boarder_profile = request.user.profile_image.url if request.user.profile_image else '/static/default.png'
                landlord_profile = landlord.profile_image.url if landlord.profile_image else '/static/default.png'

            elif isinstance(request.user, ScoutUser_Landlord):
                landlord = request.user
                boarder = ScoutUser.objects.get(userid = receiverid)
                
                boarder_profile = boarder.profile_image.url if boarder.profile_image else '/static/default.png'
                landlord_profile = request.user.profile_image.url if request.user.profile_image else '/static/default.png'
                

            new_message_list = []
            if message:
                new_message = Message.objects.create(
                    sender = request.user.usertype,
                    message = message,
                    boarder = boarder,
                    landlord = landlord
                )
                new_message_list.append(new_message)


            success_msg = 'Message Sent'

            if images:
                for image in images:
                    try:
                        img = Image.open(image)
                        img.verify()
                        new_image = Message.objects.create(
                        sender = request.user.usertype,
                        image = image,
                        boarder = boarder,
                        landlord = landlord
                        )
                        new_message_list.append(new_image)
                    except (IOError, ValidationError):
                        success_msg = 'Skipped files that are not valid Images'
            response_data = {
                'success': success_msg,
                'message_list': [
                        {
                            'sender': msg.sender,
                            'message': msg.message,
                            'image': msg.image.url if msg.image else None,
                            'time_sent': msg.date_created.strftime('%H:%M'),
                            'boarder_profile': boarder_profile,
                            'landlord_profile': landlord_profile
                        } 
                        for msg in new_message_list
                    ]
            }

            return JsonResponse(response_data, status = 200)
        except Exception as e:
            print(e)
            return JsonResponse({'error': f"{e}"}, status = 500)


# DO NOT REMOVE
def truncate_message(message, limit=50):
    if len(message) <= limit:
        return message
    return ' '.join(message[:limit].split(' ')[:-1]) + '...'

# FOR GCASH QR CODE
class generate_email_data(View):
    def get(self, request):
        try:
            if not request.GET.get('roomid'):
                return JsonResponse({'error': "Did not receive Room ID"}, status = 405)
            else:
                room = Room.objects.get(roomid = request.GET.get('roomid'))
        
            # if not request.GET.get('landlordid'):
            #     return JsonResponse({'error': "Did not receive Landlord ID"}, status = 405)
            # else:
            #     landlord = ScoutUser_Landlord.objects.get(userid = request.GET.get('landlordid'))

            public_key = "rentscout_bsit3b2023"
            template_key = "rentscout_landlord2023"
            
            response_data = {
                'landlord_email': room.building_id.building_owner.email,
                'to_name': room.building_id.building_owner.get_fullname,
                'boarder_name': request.user.get_fullname,
                'public_key': public_key,
                'template_key': template_key,
                'room_name': room.room_name
            }
        except:
            return JsonResponse({'error': "Server Error"}, status = 500)
        
        return JsonResponse(response_data, status = 200)

class notify_boarder(View):
    def get(self, request):
        try:
            reservationid = request.GET.get('reservationid', None)
            if not reservationid or reservationid is None:
                return JsonResponse({'error': "Error Reservation ID"}, status = 405)
            
            reservation = Reservation.objects.get(reservationid = reservationid)
            public_key = "rentscout_bsit3b2023"
            template_key = "rentscout_landlord2023"
            
            response_data = {
                'roomid': reservation.roomid.roomid,
                'buildingid': reservation.roomid.building_id.buildingid,
                'public_key': public_key,
                'template_key': template_key,
                'to_email': reservation.userid.email,
                'from_email': reservation.roomid.building_id.building_owner.email,
                'to_name': reservation.userid.get_fullname,
                'message': f'Good day! Your request to "{ reservation.roomid.room_name }" has been accepted. You may now continue with the payment of 20% the original price as your down payment.'
            }
            
            return JsonResponse(response_data, status = 200)
        except Exception as e:
            return JsonResponse({'error': f"{e}"}, status = 500)
        
        
class send_payment(View):
    def post(self, request):
        try:
            boarder = request.user
            roomid = request.POST.get('roomid_holder')

            if not roomid:
                return JsonResponse({'error': 'Form invalid'}, status = 405)
            
            room = Room.objects.get(roomid = roomid)
            landlord = room.building_id.building_owner
            newmessage = Message.objects.create(
                sender = "Boarder",
                message = f"{request.user.get_fullname} has sent his payment to {room.room_name}. Referal Code: {request.POST.get('referralid')}.",
                boarder = request.user,
                landlord = landlord
            )
            newmessage.save()

            form = PaymentForm(request.POST, request.FILES)
            if form.is_valid():
                payment = form.save(commit = False)
                payment.roomid = room
                payment.boarder = boarder
                payment.save()
                return JsonResponse({'success': 'Payment sent'}, status = 200)
            else:
                print(form.errors)
                return JsonResponse({'error': "Form invalid or incomplete"}, status = 405)
        except Exception as e:
            print("Payment Error: ", f'{e}') # ayaw e delete
            return JsonResponse({'error': 'Internal Server Error'}, status = 500)

class filter_payment(View):
    def get(self, request):
        try:
            buildingid = request.GET.get('buildingid', None)
            statusQ = request.GET.get('statusQ', None)
            if (not buildingid or buildingid is None) or (not statusQ or statusQ is None):
                return JsonResponse({'error': 'Bad Request'}, status = 405)
            
            building = Building.objects.get(buildingid = buildingid)
            rooms = Room.objects.filter(building_id = building)

            payments = Payment.objects.filter(
                status = statusQ,
                roomid__in = rooms
            )

            data_list = [
                {
                    'paymentid': data.paymentid,
                    'referal_code': data.referralid,
                    'payment_img': data.payment_img.url if data.payment_img else '',
                    'roomid': data.roomid.roomid,
                    'boarder': data.boarder.get_fullname,
                    'date': data.date_sent.strftime('%B %d, %Y')
                }
                for data in payments
            ]

            response_data = {
                'payments_list': data_list,

            }
        
            return JsonResponse(response_data, status = 200)
        except Exception as e:
            print(f"Error: {e}")
            return JsonResponse({'error': "Server Error"}, status = 500)

class accept_payment(View):
    def post(self, request):
        paymentid = request.POST.get('paymentid')

        if not paymentid:
            return JsonResponse({'error': 'Bad Request'}, status = 405)

        try:
            payment = Payment.objects.get(paymentid = paymentid)
            payment.status = payment.ACCEPTED
            payment.save()

            return JsonResponse({'success': "Payment accepted"}, status = 200)
        except Exception as e:
            print(f"Payment Error: {e}")
            return JsonResponse({'error': "Server error"}, status = 500)

class decline_payment(View):
    def post(self, request):
        paymentid = request.POST.get('paymentid')

        if not paymentid:
            return JsonResponse({'error': 'Bad Request'}, status = 405)

        try:
            payment = Payment.objects.get(paymentid = paymentid)
            payment.status = payment.DECLINED
            payment.save()

            return JsonResponse({'success': "Payment accepted"}, status = 200)
        except Exception as e:
            print(e)
            return JsonResponse({'error': "Server error"}, status = 500)

class hide_payment(View):
    def post(self, request):
        paymentid = request.POST.get('paymentid')

        if not paymentid:
            return JsonResponse({'error': 'Bad Request'}, status = 405)

        try:
            payment = Payment.objects.get(paymentid = paymentid)
            payment.status = payment.HIDDEN
            payment.save()
            
            return JsonResponse({'success': "Payment accepted"}, status = 200)
        except Exception as e:
            print(e)
            return JsonResponse({'error': "Server error"}, status = 500)





class generate_otp(View):
    def get(self, request):
        try:
            random_string = ''.join(random.sample(string.ascii_letters + string.digits, 6))
            public_key = "rentscout_bsit3b2023"
            template_key = "rentscout_signup2023"
            response = {
                'otp': random_string,
                'mail_keys': {
                    'public_key': public_key,
                    'template_key': template_key
                }
            }
            return JsonResponse(response, status = 200)

        except Exception as e:
            return JsonResponse({'error': f"{e}"}, status = 500)
        
# KEYS FOR TEMPLATES USING MAILJS
class get_mailjs_keys(View):
    def get(self, request):
        try: 
            public_key = "rentscout_bsit3b2023"
            template_key = "rentscout_signup2023"
            response_data = {
                'public_key': public_key,
                'template_key': template_key
            }

            return JsonResponse(response_data, status = 200)
        except Exception as e:
            return JsonResponse({'error': f"{e}"}, status = 500)


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

@receiver(post_save, sender=ScoutUser)
def log_boarder(sender, instance, created, **kwargs):
    print(f'log boarder: {created}')
    if created:
        CreatedBoarder.objects.create(
            userid = instance.userid,
            email=instance.email,
            firstname=instance.firstname,
            lastname=instance.lastname,
            middlename=instance.middlename,
            birthdate=instance.birthdate,
            gender=instance.gender,
            barangay=instance.barangay,
            province=instance.province,
            city=instance.city,
            contact=instance.contact,
        )
    else:
        UpdatedBoarder.objects.create(
            userid = instance.userid,
            email=instance.email,
            firstname=instance.firstname,
            lastname=instance.lastname,
            middlename=instance.middlename,
            birthdate=instance.birthdate,
            gender=instance.gender,
            barangay=instance.barangay,
            province=instance.province,
            city=instance.city,
            contact=instance.contact,
        )

@receiver(post_save, sender=ScoutUser_Landlord)
def log_landlord(sender, instance, created, **kwargs):
    if created:
        CreatedLandlord.objects.create(
            userid = instance.userid,
            email=instance.email,
            firstname=instance.firstname,
            lastname=instance.lastname,
            middlename=instance.middlename,
            birthdate=instance.birthdate,
            gender=instance.gender,
            barangay=instance.barangay,
            province=instance.province,
            city=instance.city,
            contact=instance.contact,
        )
    else:
        UpdatedLandlord.objects.create(
            userid = instance.userid,
            email=instance.email,
            firstname=instance.firstname,
            lastname=instance.lastname,
            middlename=instance.middlename,
            birthdate=instance.birthdate,
            gender=instance.gender,
            barangay=instance.barangay,
            province=instance.province,
            city=instance.city,
            contact=instance.contact,
        )

@receiver(post_save, sender=Building)
def building_saved(sender, instance, created, **kwargs):
    if created:
        CreatedBuilding.objects.create(
            buildingid=instance.buildingid,
            building_owner=instance.building_owner.get_fullname,
            building_name=instance.building_name,
            price=instance.price,
            zip_code=instance.zip_code,
            street=instance.street,
            city=instance.city,
            province=instance.province,
            country=instance.country,
            details=instance.details,
            coordinates=instance.coordinates,
            average_rating=instance.average_rating
        )        
    else:        
        UpdatedBuilding.objects.create(
            buildingid=instance.buildingid,
            building_owner=instance.building_owner.get_fullname,
            building_name=instance.building_name,
            price=instance.price,
            zip_code=instance.zip_code,
            street=instance.street,
            city=instance.city,
            province=instance.province,
            country=instance.country,
            details=instance.details,
            coordinates=instance.coordinates,
            average_rating=instance.average_rating
        )

@receiver(pre_delete, sender=Building)
def building_deleted(sender, instance, **kwargs):
    DeletedBuilding.objects.create(
        buildingid=instance.buildingid,
        building_owner=instance.building_owner.get_fullname,
        building_name=instance.building_name,
        price=instance.price,
        zip_code=instance.zip_code,
        street=instance.street,
        city=instance.city,
        province=instance.province,
        country=instance.country,
        details=instance.details,
        coordinates=instance.coordinates,
        average_rating=instance.average_rating,
        deleted_at=timezone.now() 
    )

@receiver(post_save, sender=Room)
def room_saved(sender, instance, created, **kwargs):
    if created:
        CreatedRoom.objects.create(
            roomid=instance.roomid,
            owner = instance.building_id.building_owner.get_fullname,
            building_name=instance.building_id.building_name,
            room_name=instance.room_name
        )
    else:
        UpdatedRoom.objects.create(
            roomid=instance.roomid,
            owner = instance.building_id.building_owner.get_fullname,
            building_name=instance.building_id.building_owner.get_fullname,
            room_name=instance.room_name
        )

@receiver(pre_delete, sender=Room)
def room_deleted(sender, instance, **kwargs):
    DeletedRoom.objects.create(
        roomid=instance.roomid,
        owner = instance.building_id.building_owner.get_fullname,
        building_name=instance.building_id.building_owner.get_fullname,
        room_name=instance.room_name
    )

# Payment Receivers
@receiver(post_save, sender=Payment)
def create_payment_record(sender, instance, created, **kwargs):
    if created:
        CreatedPayment.objects.create(
            paymentid=instance.paymentid,
            referralid=instance.referralid,
            building_name=instance.roomid.building_id.building_name,
            boarder_name=instance.boarder.get_fullname
        )
    else:
        if instance.status == Payment.ACCEPTED:
            AcceptedPayment.objects.create(
                paymentid=instance.paymentid,
                referralid=instance.referralid,
                building_name=instance.roomid.building_id.building_name,
                boarder_name=instance.boarder.get_fullname
            )
        elif instance.status == Payment.DECLINED:
            DeniedPayment.objects.create(
                paymentid=instance.paymentid,
                referralid=instance.referralid,
                building_name=instance.roomid.building_id.building_name,
                boarder_name=instance.boarder.get_fullname
            )

# Building Report Receivers
@receiver(post_save, sender=BuildingReport)
def create_report_record(sender, instance, created, **kwargs):
    if created:
        CreatedReport.objects.create(
            reportid=instance.reportid,
            building=instance.buildingid.building_name,
            reporter=instance.reporter.get_fullname,
            reason=instance.reason
        )
    else:
        AcceptedReport.objects.create(
            reportid=instance.reportid,
            building=instance.buildingid.building_name,
            reporter=instance.reporter.get_fullname,
            reason=instance.reason
        )

# Verification Receivers
@receiver(post_save, sender=Verification)
def create_verification_record(sender, instance, created, **kwargs):
    if created:
        CreatedVerification.objects.create(
            verificationid=instance.verificationid,
            building=instance.buildingid.building_name
        )
    else:
        if instance.status == Verification.VERIFIED:
            AcceptedVerification.objects.create(
                verificationid=instance.verificationid,
                building=instance.buildingid.building_name
            )
        elif instance.status == Verification.NOT_VERIFIED:
            DeniedVerification.objects.create(
                verificationid=instance.verificationid,
                building=instance.buildingid.building_name,
                reason=instance.deny_reason
            )

@receiver(pre_delete, sender=Verification)
def delete_verification_record(sender, instance, **kwargs):
    DeletedVerification.objects.create(
        verificationid=instance.verificationid,
        building=instance.buildingid.building_name,
    )





@login_required(login_url = 'signin')
def boarder_record(request, status_q):
    page = 'boarder'
    record_status = status_q
    if status_q == 'NEW':
        record = CreatedBoarder.objects.all()
    elif status_q == 'UPDATED':
        record = UpdatedBoarder.objects.all()

    context = {'page': page, 'record': record, 'record_status':record_status}
    return render(request, 'RentScout/admin/dbms_report.html', context)

@login_required(login_url = 'signin')
def landlord_record(request, status_q):
    page = 'landlord'
    record_status = status_q

    if status_q == 'NEW':
        record = CreatedLandlord.objects.all()
    elif status_q == 'UPDATED':
        record = UpdatedLandlord.objects.all()
        

    context = {'page': page, 'record': record, 'record_status':record_status}
    return render(request, 'RentScout/admin/dbms_report.html', context)

@login_required(login_url = 'signin')
def building_record(request, status_q):
    page = 'building'

    if status_q == 'NEW':
        record = CreatedBuilding.objects.all()
    elif status_q == 'UPDATED':
        record = UpdatedBuilding.objects.all()
    elif status_q == 'DELETED':
        record = DeletedBuilding.objects.all()

    context = {'page': page, 'record': record, 'record_status': status_q}
    return render(request, 'RentScout/admin/dbms_report.html', context)

@login_required(login_url = 'signin')
def room_record(request, status_q):
    page = 'room'

    if status_q == 'NEW':
        record = CreatedRoom.objects.all()
    elif status_q == 'UPDATED':
        record = UpdatedRoom.objects.all()
    elif status_q == 'DELETED':
        record = DeletedRoom.objects.all()

    context = {'page': page, 'record': record, 'record_status': status_q}
    return render(request, 'RentScout/admin/dbms_report.html', context)


@login_required(login_url = 'signin')
def payment_record(request, status_q):
    page = 'payment'

    if status_q == 'NEW':
        record = CreatedPayment.objects.all()
    elif status_q == 'ACCEPTED':
        record = AcceptedPayment.objects.all()
    elif status_q == 'DENIED':
        record = DeniedPayment.objects.all()

    context = {'page': page, 'record': record, 'record_status': status_q}
    return render(request, 'RentScout/admin/dbms_report.html', context)

@login_required(login_url = 'signin')
def report_record(request, status_q):
    page = 'report'

    if status_q == 'NEW':
        record = CreatedReport.objects.all()
    elif status_q == 'ACCEPTED':
        record = AcceptedReport.objects.all()
    elif status_q == 'DENIED':
        record = DeniedReport.objects.all()

    context = {'page': page, 'record': record, 'record_status': status_q}
    return render(request, 'RentScout/admin/dbms_report.html', context)

@login_required(login_url = 'signin')
def verification_record(request, status_q):
    page = 'verification'

    if status_q == 'NEW':
        record = CreatedVerification.objects.all()
    elif status_q == 'ACCEPTED':
        record = AcceptedVerification.objects.all()
    elif status_q == 'DENIED':
        page = 'verification_denied'
        record = DeniedVerification.objects.all()
    elif status_q == 'DELETED':
        record = DeletedVerification.objects.all()

    context = {'page': page, 'record': record, 'record_status': status_q}
    return render(request, 'RentScout/admin/dbms_report.html', context)
