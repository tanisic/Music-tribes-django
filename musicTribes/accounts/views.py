from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
def profile(request,user_id):
    user_profile = User.objects.filter(id=user_id).first()