from django.db import models
from django.db.models import constraints
from django.utils import timezone
from django.contrib.auth.models import User

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
    chieftain=models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(unique=True,max_length=50,blank=False)
    def chieftain(self):
        return self.chieftain

    def created_by(self):
        return self.chieftain.username
    
    def __str__(self):
        return self.name

class Song(TimeStamped):
    url = models.CharField(max_length=60,unique=True,blank=False)
    title = models.CharField(blank=False,max_length=200)
    creator = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Playlist(TimeStamped):
    tribe = models.ForeignKey(Tribe,on_delete=models.CASCADE)
    name = models.CharField(unique=True,blank=False,max_length=128)
    creator = models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    songs = models.ManyToManyField(Song)

    def __str__(self):
        return self.name

class Comment(TimeStamped):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist,on_delete=models.CASCADE)
    text = models.TextField(blank=False)

class Like(TimeStamped):
    song = models.ForeignKey(Song,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    like = models.BooleanField(null=False,default=True)

    class Meta:
        constraints=[
            models.UniqueConstraint(name='user_like',fields=['user','song'])
        ]

    def liked(self):
        return self.like

