from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm


class ExtendedUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class EditUserForm(ExtendedUserCreationForm):
    class Meta:
        model = User
        fields=('first_name','last_name','email', 'password1', 'password2')