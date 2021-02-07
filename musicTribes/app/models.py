from django.db import models
from django.db.models import constraints
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Profile

class TimeStamped(models.Model):
    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField(editable=False)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()

        self.updated_at = timezone.now()
        return super(TimeStamped, self).save(*args, **kwargs)

    class Meta:
        abstract = True

class Tribe(TimeStamped):
    chieftain = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    name = models.CharField(unique=True,max_length=50,blank=False)
    logourl =  models.CharField(max_length=1000,default="https://image.shutterstock.com/image-vector/hand-drawn-tribal-label-textured-260nw-471977746.jpg",blank=False)
    logo_img = models.ImageField(upload_to='images/tribes',blank = True) 
    genre = models.CharField(max_length=100,blank=False)

    def author(self):
        return self.chieftain

    def created_by(self):
        return self.chieftain.user.username
    
    def __str__(self):
        return self.name


class Playlist(TimeStamped):
    tribe = models.ForeignKey(Tribe,on_delete=models.CASCADE)
    name = models.CharField(unique=False,blank=False,max_length=128)
    creator = models.ForeignKey(Profile,on_delete=models.CASCADE,default=1)
    description = models.TextField(max_length=1000)
    
    def __str__(self):
        return self.name

    def created_by(self):
        return self.chieftain.user.username

class Song(TimeStamped):
    url = models.CharField(max_length=60,unique=False,blank=False)
    title = models.CharField(blank=False,max_length=200)
    creator = models.ForeignKey(Profile,on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist,on_delete=models.CASCADE)
    

    

    def __str__(self):
        return self.title

class Message(TimeStamped):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    tribe = models.ForeignKey(Tribe,on_delete=models.CASCADE)
    text  = models.TextField(blank=False)

class Comment(TimeStamped):
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist,on_delete=models.CASCADE)
    text = models.TextField(blank=False)

class Like(TimeStamped):
    song = models.ForeignKey(Song,on_delete=models.CASCADE)
    user = models.ForeignKey(Profile,on_delete=models.CASCADE)

    class Meta:
        constraints=[
            models.UniqueConstraint(name='user_like',fields=['user','song'])
        ]
    


