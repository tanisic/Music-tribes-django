from accounts.models import Profile
from .models import *

def is_member_of_tribe(user,tribe):
    profile = Profile.objects.get(user=user)
    if is_chieftain(profile,tribe):
        True
    if tribe in profile.tribes.all():
        return True
    else:
        return False

def like_count_song(song):
    likes_count = Like.objects.filter(song=song).count()
    return likes_count

def is_chieftain(profile,tribe):
    if profile == tribe.chieftain:
        return True
    else:
        return False