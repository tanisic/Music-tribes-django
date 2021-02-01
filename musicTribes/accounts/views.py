from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic

class ExtendedUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class SignUpView(generic.CreateView):
    form_class=ExtendedUserCreationForm
    success_url= reverse_lazy('login')
    template_name = 'registration/signup.html'

# Create your views here.
def profile(request,user_id):
    user_profile = User.objects.filter(id=user_id).first()