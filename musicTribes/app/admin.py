from django.contrib import admin
from .models import Tribe,Playlist,Song,Like,Comment
# Register your models here.

admin.site.register(Tribe)
admin.site.register(Playlist)
admin.site.register(Song)
admin.site.register(Like)
admin.site.register(Comment)
