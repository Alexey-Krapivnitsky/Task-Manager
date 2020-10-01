from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password

from .models import User


class AuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return None
        else:
            return user if check_password(password, user.password) else None

    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None
