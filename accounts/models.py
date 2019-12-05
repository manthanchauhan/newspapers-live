from django.db import models
from django.contrib.auth.models import User
from accounts.validators import validate_username
from sessions.models import Session
# Create your models here.


class CustomUser(User):
    username = models.CharField(max_length=20, help_text='please use only numbers and alphabets',
                                primary_key=True, verbose_name='Username', validators=[validate_username]
                                )
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=300, help_text='use at least 8 characters')
    current_session_id = models.OneToOneField(to=Session, on_delete=models.PROTECT, related_name='+',
                                              null=True)

    class Meta:
        ordering = ['username']
        verbose_name = 'user'



