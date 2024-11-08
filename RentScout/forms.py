from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AuthenticationForm
from .models import ( ScoutUser, ScoutUser_Landlord, Building, Highlights, 
                     Policies, Room, Feedback, RoomImage, 
                     ScoutUserBookmark, LandlordUserBookmark, BuildingReport,
                     Verification,
                    )


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
                  'middlename', 'gender', 'password1', 'password2', )
                   #'barangay', 'province', 'city', 'contact' ) # 

class ScoutUserChangeForm(UserChangeForm):
    class Meta:
        model = ScoutUser
        fields = ('firstname', 'lastname', 'middlename',
                  'birthdate', 'gender',)

class ScoutUserProfileForm(UserChangeForm):
    class Meta:
        model = ScoutUser
        fields = ('firstname', 'lastname', 'middlename',
                  'birthdate', 'gender', 'barangay', 
                  'province', 'city', 'contact',)
        
    barangay = forms.CharField(required=False)
    province = forms.CharField(required=False)
    city = forms.CharField(required=False)
    contact = forms.CharField(required=False)

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

class LandlordUserProfileForm(UserChangeForm):
    class Meta:
        model = ScoutUser_Landlord
        fields = ('firstname', 'lastname', 'middlename',
                  'birthdate', 'gender', 'barangay', 
                  'province', 'city', 'contact',)

    barangay = forms.CharField(required=False)
    province = forms.CharField(required=False)
    city = forms.CharField(required=False)
    contact = forms.CharField(required=False)

class UserLoginForm(AuthenticationForm):
    pass 

class BuildingForm(ModelForm):
    class Meta:
        model = Building
        exclude = ('buildingid', 'building_owner', 'average_rating')

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

class RoomFormAdmin(ModelForm):
    class Meta:
        model = Room
        exclude = ('roomid', )

class FeedBackForm(ModelForm):
    class Meta:
        model = Feedback
        exclude = ('feedbackid', 'userid')

class RoomImageForm(ModelForm):
    class Meta:
        model = RoomImage
        exclude = ('room_imgID',)
    
class ScoutBookmarkForm(ModelForm):
    class Meta:
        model = ScoutUserBookmark
        fields = ('buildingid', )
        
class LandlordBookmarkForm(ModelForm):
    class Meta:
        model = LandlordUserBookmark
        fields = ('buildingid', )

class BuildingReportForm(ModelForm):
    class Meta:
        model = BuildingReport
        exclude = ('reportid', 'reporter', 'date_reported', )

# trash
class ScrapperFile(forms.Form):
    file = forms.FileField()

class BuildingScrapper(ModelForm):
    class Meta:
        model = Building
        exclude = ('buildingid', 'building_owner')


    # def clean_file(self):
    #     uploaded_file = self.cleaned_data.get('file')
        
    #     # Validate file size
    #     max_file_size = 10 * 1024 * 1024  # 10 MB
    #     if uploaded_file.size > max_file_size:
    #         raise forms.ValidationError("File size should not exceed 10MB.")
        
    #     # Validate file type
    #     if not uploaded_file.name.endswith('.csv'):
    #         raise forms.ValidationError("File must be a CSV file.")
        
    #     return uploaded_file