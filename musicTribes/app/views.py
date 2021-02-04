from .forms import TribeForm, PlaylistForm, SongForm
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
    is_member = False
    if request.user.is_authenticated:
        if tribe in request.user.profile.tribes.all(): 
            is_member = True
    playlists = Playlist.objects.filter(tribe=tribe)
    context={"tribe":tribe, 
            "playlists":playlists,
            "is_member":is_member
            }

    return render(request,"app/tribe.html",context)

def playlist(request,tribe_id,playlist_id):
    tribe = get_object_or_404(Tribe,pk = tribe_id)
    playlist = Playlist.objects.filter(tribe=tribe,pk=playlist_id)
    songs = Song.objects.filter(playlist=playlist.first())
    playlist = playlist[0]
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

def update_tribe(request, tribe_id):
    
    tribe = get_object_or_404(Tribe, pk=tribe_id)
    if request.method == 'POST' and (tribe.creator == request.user):
        form = TribeForm(request.POST, instance = tribe)
        if form.is_valid():
            saved_tribe = form.save()
            return HttpResponseRedirect(reverse('app:tribe', args=(saved_tribe.id,)))
    else:
        form = TribeForm(instance=tribe)
        
    context = { 'form':form, 'action':'update', }
    return render(request, 'app/update_tribe.html', context)


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

def create_song(request,playlist_id):
    if request.method == 'POST' and request.user.is_authenticated:
        form = SongForm(request.POST)
        if form.is_valid():
            saved_song = form.save(commit=False)
            saved_song.creator = request.user
            saved_song.playlist = get_object_or_404(Playlist,pk=playlist_id)
            saved_song.save()
            tribe = saved_song.playlist.tribe         
            return HttpResponseRedirect(reverse('app:playlist',args=(tribe.id,playlist_id)))
    else:
        form = SongForm()
    context = {'form':form, 'action':'create'}
    return render(request,'app/create_song.html',context)

def join(request,tribe_id):
    tribe = Tribe.objects.get(id=tribe_id)
    if request.method == 'POST' and request.user.is_authenticated:
        profile = request.user.profile
        profile.tribes.add(tribe)
        
        return HttpResponseRedirect(reverse('app:tribe',args=(tribe_id,)))
    else:
        context = {"tribe":tribe}
        return render(request,"app/tribe.html",context)
