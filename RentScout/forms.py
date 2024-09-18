from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from .models import ( ScoutUser, Building, Facilities, Policies, Room, Feedback)


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
                  'middlename', 'birthdate', 'gender', 'password1', 'password2' ) # 

class ScoutUserChangeForm(UserChangeForm):
    class Meta:
        model = ScoutUser
        fields = ('firstname', 'lastname', 'middlename',
                  'birthdate', 'gender',)
        
class UserLoginForm(AuthenticationForm):
    pass 

class BuildingForm(ModelForm):
    class Meta:
        model = Building
        exclude = ('buildingid',)

class PoliciesForm(ModelForm):
    class Meta:
        model = Policies
        exclude = ('policy_id',)

class FacilitiesForm(ModelForm):
    class Meta:
        model = Facilities
        exclude = ('facil_id',)

class RoomForm(ModelForm):
    class Meta:
        model = Room
        exclude = ('roomid',)
class FeedBackForm(ModelForm):
    class Meta:
        model = Feedback
        exclude = ('feedbackid',)
