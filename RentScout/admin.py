from django.contrib import admin
from .models import (ScoutUser, Building, Policies, Highlights, Room,
                     Feedback, RoomImage, ScoutUser_Landlord, AdminUser,
                     ScoutUserBookmark, LandlordUserBookmark, BuildingReport,
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
                    'barangay', 'province', 'city', 'contact']
    form = ScoutUserCreationForm

# Use 'password' as a read-only field to avoid exposing it directly
    readonly_fields = ('password',)
    
class ScoutUser_LandlordAdmin(admin.ModelAdmin):
    list_display = ['userid', 'email', 'firstname', 'lastname',
                    'middlename', 'gender', 'birthdate',
                    'barangay', 'province', 'city', 'contact']

    form = LandlordUserCreationForm


class BuildingAdmin(admin.ModelAdmin):
    list_display = [ 'buildingid', 'building_name', 'zip_code', 'street', 'city',
                    'province', 'country', 'details', 'rooms_vacant', 'average_rating',
                    ]
    form = BuildingFormAdmin
    
class PoliciesAdmin(admin.ModelAdmin):
    list_display = ['policy_id', 'buildingid', 'policy']

class HighlightsAdmin(admin.ModelAdmin):
    list_display = ['highlights_id', 'buildingid', 'free_wifi', 'shared_kitchen', 
                    'smoke_free', 'janitor', 'waterbill', 'electricbill', 
                    'guard', 'food']
    
class RoomAdmin(admin.ModelAdmin):
    list_display = ['roomid','room_name', 'get_building_name'] #'buildingid', , 'person_free',
                    #'current_male', 'current_female', 'price', 'room_size',
                   #'shower', 'priv_bathroom', 'public_bathroom', 'AC', 'wardrobe',
                   #'kitchen', 'bedroom', 'double_deck', 'free_wifi'
    form = RoomFormAdmin

    def get_building_name(self, obj):
        return obj.building_id.building_name

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['feedbackid', 'boardingid', 'rating', 'message']

class RoomImageAdmin(admin.ModelAdmin):
    list_display = ['room_imgID', 'get_room_name']
    form = RoomImageForm

    def get_room_name(self, obj):
            return obj.roomid.room_name
    

class ScoutBookmarkAdmin(admin.ModelAdmin):
    list_display = ['buildingid', 'owner']

class LandlordBookmarkAdmin(admin.ModelAdmin):
    list_display = ['buildingid', 'owner']


class BuildingReportAdmin(admin.ModelAdmin):
    list_display = ['reportid', 'date_reported', 'reason']

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