from django.contrib import admin
from .models import (ScoutUser, Building, Policies, Facilities, Room,
                     Feedback)
from .forms import (UserCreationForm, UserChangeForm, ScoutUserCreationForm)
# Register your models here.

class ScoutUserAdmin(admin.ModelAdmin):
    list_display = ['userid', 'firstname', 'lastname',
                    'middlename', 'gender', 'birthdate']
    form = ScoutUserCreationForm

# Use 'password' as a read-only field to avoid exposing it directly
    readonly_fields = ('password',)
    
class BuildingAdmin(admin.ModelAdmin):
    list_display = [ 'buildingid', 'building_name', 'zip_code', 'street', 'city',
                    'province', 'country', 'details', 'rooms_vacant']

class PoliciesAdmin(admin.ModelAdmin):
    list_display = ['policy_id', 'buildingid', 'policy']

class FacilitiesAdmin(admin.ModelAdmin):
    list_display = ['facil_id', 'buildingid', 'free_wifi', 'shared_kitchen', 
                    'smoke_free', 'janitor', 'waterbill', 'electricbill', 
                    'comfort_room', 'food']
    
class RoomAdmin(admin.ModelAdmin):
    list_diplay = ['roomid', 'buildingid', 'room_name', 'person_free',
                   'current_male', 'current_female', 'price', 'room_size',
                   'shower', 'priv_bathroom', 'public_bathroom', 'AC', 'wardrobe',
                   'kitchen', 'bedroom', 'double_deck', 'free_wifi']

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['feedbackid', 'boardingid', 'rating', 'message']

admin.site.register(ScoutUser, ScoutUserAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(Policies, PoliciesAdmin)
admin.site.register(Facilities, FacilitiesAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Feedback, FeedbackAdmin)
