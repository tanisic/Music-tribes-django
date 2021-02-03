from django.db.models.base import Model
from .models import Playlist, Song, Tribe
from django.forms import ModelForm, fields

class TribeForm(ModelForm):
    class Meta:
        model = Tribe
        fields = ['name', 'genre', 'logourl']

class PlaylistForm(ModelForm):
    class Meta:
        model = Playlist
        fields = ['tribe','name',]

class SongForm(ModelForm):
    class Meta:
        model = Song
        fields = ['title','url']