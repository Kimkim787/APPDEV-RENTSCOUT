from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from .models import ( ScoutUser, ScoutUser_Landlord, Building, Highlights, 
                     Policies, Room, Feedback, RoomImage, BuildingImage)


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(widget = forms.EmailInput(attrs = {'autofocus': True}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'

    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password :
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code = 'invalid_login',
                    params = {'username': email},
                )
            
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

class ScoutUserCreationForm(UserCreationForm):
    class Meta:
        model = ScoutUser
        fields = ('email', 'firstname', 'lastname',
                  'middlename', 'gender', 'password1', 'password2' ) # 

class ScoutUserChangeForm(UserChangeForm):
    class Meta:
        model = ScoutUser
        fields = ('firstname', 'lastname', 'middlename',
                  'birthdate', 'gender',)

class LandlordUserCreationForm(UserCreationForm):
    class Meta:
        model = ScoutUser_Landlord
        fields = ('email', 'firstname', 'lastname',
                  'middlename', 'gender', 'password1', 'password2' ) # 

class LandlordUserChangeForm(UserChangeForm):
    class Meta:
        model = ScoutUser_Landlord
        fields = ('firstname', 'lastname', 'middlename',
                  'birthdate', 'gender',)

class UserLoginForm(AuthenticationForm):
    pass 

class BuildingForm(ModelForm):
    class Meta:
        model = Building
        exclude = ('buildingid', 'building_owner')

class BuildingFormAdmin(ModelForm):
    class Meta:
        model = Building
        exclude = ('buildingid',)

class PoliciesForm(ModelForm):
    class Meta:
        model = Policies
        exclude = ('policy_id', 'buildingid')

# class PolicyUpdateForm(ModelForm):
#     class Meta:
#         model = Policies
#         exclude = ('policy_id', 'building_id')

class HighlightsForm(ModelForm):
    class Meta:
        model = Highlights
        exclude = ('highlights_id','buildingid') # 

class RoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = ('roomid','building_id')

class FeedBackForm(ModelForm):
    class Meta:
        model = Feedback
        exclude = ('feedbackid', 'userid')

class RoomImageForm(ModelForm):
    class Meta:
        model = RoomImage
        exclude = ('room_imgID',)
    
class BuildingImageForm(ModelForm):
    class Meta:
        model = BuildingImage
        exclude = ('building_imgID', 'building_img')
