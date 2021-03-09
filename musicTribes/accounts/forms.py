from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm
from app.models import Profile
from django.utils.translation import gettext as _


class ExtendedUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=('email','first_name','last_name')

class EditProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('avatarurl','avatar_img','bio')
    
class ChangePasswordForm(UserCreationForm):
    class Meta:
        model = User
        fields=('password1','password2')
