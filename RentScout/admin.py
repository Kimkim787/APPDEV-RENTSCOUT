from django.contrib import admin
from .models import (ScoutUser, Building, Policies, Highlights, Room,
                     Feedback, RoomImage, ScoutUser_Landlord)
from .forms import (UserCreationForm, UserChangeForm, ScoutUserCreationForm, BuildingForm,
                    RoomForm, RoomImageForm, LandlordUserCreationForm, BuildingFormAdmin)
# Register your models here.

class ScoutUserAdmin(admin.ModelAdmin):
    list_display = ['userid', 'firstname', 'lastname',
                    'middlename', 'gender', 'birthdate']
    form = ScoutUserCreationForm

# Use 'password' as a read-only field to avoid exposing it directly
    readonly_fields = ('password',)
    
class ScoutUser_LandlordAdmin(admin.ModelAdmin):
    list_display = ['userid', 'firstname', 'lastname',
                    'middlename', 'gender', 'birthdate']
    form = LandlordUserCreationForm


class BuildingAdmin(admin.ModelAdmin):
    list_display = [ 'buildingid', 'building_name', 'zip_code', 'street', 'city',
                    'province', 'country', 'details', 'rooms_vacant']
    form = BuildingFormAdmin
    
class PoliciesAdmin(admin.ModelAdmin):
    list_display = ['policy_id', 'buildingid', 'policy']

class HighlightsAdmin(admin.ModelAdmin):
    list_display = ['highlights_id', 'buildingid', 'free_wifi', 'shared_kitchen', 
                    'smoke_free', 'janitor', 'waterbill', 'electricbill', 
                    'guard', 'food']
    
class RoomAdmin(admin.ModelAdmin):
    list_display = ['roomid','room_name'] #'buildingid', , 'person_free',
                    #'current_male', 'current_female', 'price', 'room_size',
                   #'shower', 'priv_bathroom', 'public_bathroom', 'AC', 'wardrobe',
                   #'kitchen', 'bedroom', 'double_deck', 'free_wifi'
    form = RoomForm

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['feedbackid', 'boardingid', 'rating', 'message']

class RoomImageAdmin(admin.ModelAdmin):
    list_display = ['room_imgID', 'get_room_name', 'room_imgID']
    form = RoomImageForm

    def get_room_name(self, obj):
            return obj.roomid.room_name
    
admin.site.register(ScoutUser, ScoutUserAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Policies, PoliciesAdmin)
admin.site.register(Highlights, HighlightsAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(RoomImage, RoomImageAdmin)
admin.site.register(ScoutUser_Landlord, ScoutUser_LandlordAdmin)