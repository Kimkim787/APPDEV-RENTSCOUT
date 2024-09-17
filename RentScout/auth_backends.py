from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import ScoutUser

class ScoutUserBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = ScoutUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except ScoutUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return ScoutUser.objects.get(pk=user_id)
        except ScoutUser.DoesNotExist:
            return None
