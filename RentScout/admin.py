from django.contrib import admin
from .models import (ScoutUser, Building, Policies, Highlights, Room,
                     Feedback, RoomImage, ScoutUser_Landlord, AdminUser,
                     ScoutUserBookmark, LandlordUserBookmark, BuildingReport,
                     Verification, Reservation, Message, Payment, Certificate,
                     CreatedBoarder, CreatedBuilding, UpdatedBuilding, DeletedBuilding,
                     CreatedRoom, UpdatedRoom, DeletedRoom, 
                     )   
from .forms import (UserCreationForm, UserChangeForm, ScoutUserCreationForm, BuildingForm,
                    RoomForm, RoomImageForm, LandlordUserCreationForm, BuildingFormAdmin,
                    RoomFormAdmin, LandlordUserProfileForm, ScoutUserProfileForm,
                    ScoutBookmarkForm, LandlordBookmarkForm)
# Register your models here.

class AdminUserAdmin(admin.ModelAdmin):
    list_display = ['userid', 'email', 'username']
    
class ScoutUserAdmin(admin.ModelAdmin):
    list_display = ['userid', 'email', 'firstname', 'lastname',
                    'middlename', 'gender', 'birthdate', 
                    'barangay', 'province', 'city', 'contact', 'profile_image', 'verified', 'date_joined']
    form = ScoutUserCreationForm

# Use 'password' as a read-only field to avoid exposing it directly
    readonly_fields = ('password',)
    
class ScoutUser_LandlordAdmin(admin.ModelAdmin):
    list_display = ['userid', 'email', 'firstname', 'lastname',
                    'middlename', 'gender', 'birthdate',
                    'barangay', 'province', 'city', 'contact', 'profile_image', 'verified', 'date_joined']

    form = LandlordUserCreationForm


class BuildingAdmin(admin.ModelAdmin):
    list_display = [ 'buildingid', 'building_name', 'zip_code', 'street', 'city',
                    'province', 'country', 'details', 'rooms_vacant', 'coordinates', 'average_rating',
                    'building_image', 'gcash_qr'
                    ]
    form = BuildingFormAdmin
    
class PoliciesAdmin(admin.ModelAdmin):
    list_display = ['policy_id', 'buildingid', 'policy']

class HighlightsAdmin(admin.ModelAdmin):
    list_display = ['highlights_id', 'buildingid', 'free_wifi', 'shared_kitchen', 
                    'smoke_free', 'janitor', 'waterbill', 'electricbill', 
                    'guard', 'food']
    
class RoomAdmin(admin.ModelAdmin):
    list_display = ['roomid','room_name', 'building_id', 'get_building_name', 'person_free',
                    'current_male', 'current_female', 'room_size',
                   'shower', 'priv_bathroom', 'public_bathroom', 'AC', 'wardrobe',
                   'kitchen', 'bed', 'double_deck', 'free_wifi']
    form = RoomFormAdmin

    def get_building_name(self, obj):
        return obj.building_id.building_name

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['feedbackid', 'boardingid', 'userid', 'rating', 'message']

class RoomImageAdmin(admin.ModelAdmin):
    list_display = ['room_imgID', 'roomid', 'get_room_name', 'room_img']
    form = RoomImageForm

    def get_room_name(self, obj):
            return obj.roomid.room_name
    

class ScoutBookmarkAdmin(admin.ModelAdmin):
    list_display = ['buildingid', 'owner']

class LandlordBookmarkAdmin(admin.ModelAdmin):
    list_display = ['buildingid', 'owner']


class BuildingReportAdmin(admin.ModelAdmin):
    list_display = ['reportid', 'buildingid', 'reporter', 'date_reported', 'reason']

class ReservationAdmin(admin.ModelAdmin):
    list_display = ['reservationid', 'roomid', 'userid', 'status', 'created', 'last_updated']
    
    def room_name(self, obj):
            return obj.roomid.room_name if obj.roomid else '-'
        
    def user_fullname(self, obj):
        return obj.userid.get_fullname if obj.userid else '-'
    
    room_name.admin_order_field = 'roomid__room_name'
    user_fullname.admin_order_field = 'userid__first_name'
    
    room_name.short_description = 'Room'
    user_fullname.short_description = 'User'

class VerificationAdmin(admin.ModelAdmin):
    list_display = ['verificationid', 'buildingid', 'status', 'date_requested']

class CertificateAdmin(admin.ModelAdmin):
    list_display = ['certificationid', 'buildingid', 'certificate_name', 'image', 'date_uploaded']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['messageid', 'sender', 'message', 'image', 'boarder', 'landlord', 'date_created']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['paymentid', 'referralid', 'payment_img', 'roomid', 'boarder', 'status',
                    'date_sent']
    
admin.site.register(ScoutUser, ScoutUserAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Policies, PoliciesAdmin)
admin.site.register(Highlights, HighlightsAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(RoomImage, RoomImageAdmin)
admin.site.register(ScoutUser_Landlord, ScoutUser_LandlordAdmin)
admin.site.register(ScoutUserBookmark, ScoutBookmarkAdmin)
admin.site.register(LandlordUserBookmark, LandlordBookmarkAdmin)
admin.site.register(AdminUser, AdminUserAdmin)
admin.site.register(BuildingReport, BuildingReportAdmin)
admin.site.register(Verification)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Certificate, CertificateAdmin)
