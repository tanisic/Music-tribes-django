from django.contrib import admin
from .models import Tribe,Playlist,Song,Comment,Profile,Message
# Register your models here.

admin.site.register(Profile)
admin.site.register(Tribe)
admin.site.register(Playlist)
admin.site.register(Song)
admin.site.register(Comment)
admin.site.register(Message)
