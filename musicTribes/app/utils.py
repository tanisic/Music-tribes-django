from accounts.models import Profile
from .models import *

def is_member_of_tribe(user,tribe):
    profile = Profile.objects.filter(user=user).first()
    if tribe in profile.tribes.all():
        return True
    else:
        return False

def like_count_song(song):
    likes_count = Like.objects.filter(song=song).count()
    return likes_count