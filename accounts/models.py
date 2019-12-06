from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from accounts.validators import validate_username
# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, username, password, email, is_staff=False, is_superuser=False, is_active=False):
        user = self.model(username=username, email=email, is_staff=is_staff, is_active=is_active,
                          is_superuser=is_superuser)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password):
        return self.create_user(username, password, email, is_staff=True, is_superuser=True, is_active=True)


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=20, help_text='please use only numbers and alphabets',
                                primary_key=True, verbose_name='Username', validators=[validate_username]
                                )
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300, help_text='use at least 8 characters')
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    current_session_id = models.IntegerField(unique=True, null=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        ordering = ['username']
        verbose_name = 'user'

    def has_module_perms(self, app_label):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return self.is_superuser



