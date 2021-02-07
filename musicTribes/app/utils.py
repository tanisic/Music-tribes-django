from accounts.models import Profile
from .models import *

def is_member_of_tribe(user,tribe):
    profile = Profile.objects.filter(user=user).first()
    if tribe in profile.tribes.all():
        return True
    else:
        return False

def user_liked_song(user,song):
    profile = Profile.objects.filter(user=user).first()
    if profile in song.likes.all():
        return True
    else:
        return False