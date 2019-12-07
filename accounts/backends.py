from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password
from accounts.models import CustomUser
from django.core.exceptions import ObjectDoesNotExist


class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        print(username, password)
        try:
            user = CustomUser.objects.get(username=username)
        except ObjectDoesNotExist:
            return None

        print(user.email)

        if check_password(password, user.password):
            return user
        else:
            return None
