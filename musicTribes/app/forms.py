from django.db.models.base import Model
from .models import Message, Playlist, Song, Tribe
from django.forms import ModelForm, fields

class TribeForm(ModelForm):
    class Meta:
        model = Tribe
        fields = ['name', 'genre', 'logourl','logo_img']

class PlaylistForm(ModelForm):
    class Meta:
        model = Playlist
        fields = ['name','description']

class SongForm(ModelForm):
    class Meta:
        model = Song
        fields = ['title','url']

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['text']

