from django.contrib.auth.forms import UserCreationForm
from django import forms
from accounts.models import CustomUser


class SignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")
        widgets = {"email": forms.EmailInput(attrs={"disabled": True})}
