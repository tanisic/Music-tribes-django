from .forms import TribeForm, PlaylistForm
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Playlist, Tribe, Song

# Create your views here.
def index(request):
    tribes = Tribe.objects.order_by("created_at")
    context={"tribes":tribes}

    return render(request,"app/index.html",context)

def tribe(request,tribe_id):
    tribe = get_object_or_404(Tribe,pk=tribe_id)
    playlists = Playlist.objects.filter(tribe=tribe)
    context={"tribe":tribe, 
            "playlists":playlists}

    return render(request,"app/tribe.html",context)

def playlist(request,tribe_id,playlist_id):
    tribe = get_object_or_404(Tribe,pk = tribe_id)
    playlist = Playlist.objects.filter(tribe=tribe,pk=playlist_id)
    playlist = playlist[0]
    songs = playlist.songs.all()
    context={"playlist":playlist,
            "songs":songs}

    return render(request,"app/playlist.html",context)

def create_tribe(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = TribeForm(request.POST)
        if form.is_valid():
            saved_tribe = form.save(commit=False)
            saved_tribe.creator = request.user
            saved_tribe.save()
            return HttpResponseRedirect(reverse('app:tribe',args=(saved_tribe.id,)))
    else:
        form = TribeForm()
    context = {'form':form, 'action':'create'}
    return render(request,'app/create_tribe.html',context)

def create_playlist(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = PlaylistForm(request.POST)
        if form.is_valid():
            saved_playlist = form.save(commit=False)
            saved_playlist.creator = request.user
            saved_playlist.save()
            return HttpResponseRedirect(reverse('app:playlist',args=(saved_playlist.tribe.id,saved_playlist.id,)))
    else:
        form = PlaylistForm()
    context = {'form':form, 'action':'create'}
    return render(request,'app/create_playlist.html',context)