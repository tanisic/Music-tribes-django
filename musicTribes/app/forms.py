from django.db.models.base import Model
from .models import Comment, Message, Playlist, Song, Tribe
from django.forms import ModelForm, fields
from bootstrap_datepicker_plus import TimePickerInput
from musicTribes import settings

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
        fields = ['artist','title','url','song_duration']
        widgets = {'song_duration': TimePickerInput(options={"useCurrent":True,})} 
    


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['text']

class CommentForm(ModelForm):
    class Meta:
        model=Comment
        fields = ['text']

