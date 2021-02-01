from django.db.models.base import Model
from .models import Playlist, Tribe
from django.forms import ModelForm, fields

class TribeForm(ModelForm):
    class Meta:
        model = Tribe
        fields = ['name']

class PlaylistForm(ModelForm):
    class Meta:
        model = Playlist
        fields = ['tribe','name','songs']