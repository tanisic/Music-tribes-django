from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

import app


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True)
    avatarurl =  models.CharField(max_length=1000,default="https://icon-library.com/images/unknown-person-icon/unknown-person-icon-17.jpg",blank=True)
    tribes = models.ManyToManyField('app.Tribe',blank=True)
    avatar_img = models.ImageField(upload_to='images',blank = True) 

    def __str__(self):
        return self.user.username

    


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
