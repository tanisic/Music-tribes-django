from .forms import MessageForm, TribeForm, PlaylistForm,SongForm, CommentForm
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Playlist, Tribe, Song, Profile
from .utils import *
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        tribes = Tribe.objects.order_by("created_at")
        chieftain_tribes_id = []
        for tribe in tribes:
            if tribe.chieftain == request.user.profile:
                chieftain_tribes_id.append(tribe.id)

        chieftain_tribes = Tribe.objects.filter(id__in = chieftain_tribes_id)

        member_tribes_id = []
        for tribe in tribes:
            for user_tribe in request.user.profile.tribes.all():
                if tribe == user_tribe:
                    member_tribes_id.append(tribe.id)

        member_tribes = Tribe.objects.filter(id__in = member_tribes_id)

        discover_tribes_id =[]
        for tribe in tribes:
            if not tribe.id in chieftain_tribes_id and not tribe.id in member_tribes_id:
                discover_tribes_id.append(tribe.id)
        
        discover_tribes = Tribe.objects.filter(id__in = discover_tribes_id)

        context = {"chieftain_tribes":chieftain_tribes,
                    "member_tribes": member_tribes,
                    "discover_tribes": discover_tribes}
        return render(request,"app/index.html",context)

    else:
        tribes = Tribe.objects.order_by("created_at")
        context={"tribes":tribes}

        return render(request,"app/index.html",context)

def tribe(request,tribe_id):
    tribe = get_object_or_404(Tribe,pk=tribe_id)
    profiles = Profile.objects.all()
    tribe_members_id = []
    for profile in profiles:
        if tribe in profile.tribes.all():
            tribe_members_id.append(profile.id)        
    playlists = Playlist.objects.filter(tribe=tribe)
    messages = Message.objects.filter(tribe=tribe)
    tribe_members = Profile.objects.filter(id__in=tribe_members_id)
    if request.user.is_authenticated:
        is_member = is_member_of_tribe(request.user,tribe)
    else:
        is_member=False

    is_chieftain_of_tribe = False
    if request.user.is_authenticated:
        is_chieftain_of_tribe = is_chieftain(request.user.profile,tribe)

    context={"tribe":tribe,
            "tribe_members":tribe_members, 
            "playlists":playlists,
            "is_member_of_tribe": is_member,
            "messages" : messages,
            "form":MessageForm(),
            "is_chieftain": is_chieftain_of_tribe
            }

    return render(request,"app/tribe.html",context)

def playlist(request,tribe_id,playlist_id):
    tribe = get_object_or_404(Tribe,pk = tribe_id)
    playlist = Playlist.objects.filter(tribe=tribe,pk=playlist_id)
    songs = Song.objects.filter(playlist=playlist.first())
    comments=Comment.objects.all()
    likes = []
    like_count = []

    for song in songs:
        like_count.append(like_count_song(song))
        if request.user.is_authenticated:
            if Like.objects.filter(song=song,user=request.user.profile).exists():
                likes.append(True)
            else:
                likes.append(False)
        else:
            likes.append(False)

    playlist = playlist[0]

    if request.user.is_authenticated:
        is_member = is_member_of_tribe(request.user,tribe)
    else:
        is_member = False

    context={"playlist":playlist,
            "songs_with_likes":zip(songs,likes,like_count),
            "tribe":tribe,
            "is_member_of_tribe": is_member,
            "comments":comments,
            "form":CommentForm(),
            }

    return render(request,"app/playlist.html",context)

def create_tribe(request):
    if request.method == 'POST' and request.user.is_authenticated:
        form = TribeForm(request.POST, request.FILES)
        form.fields['logourl'].initial ="https://i.pinimg.com/originals/44/e5/6f/44e56f6eb0888ac03af36df69cd6f031.png"
        if form.is_valid():
            saved_tribe = form.save(commit=False)
            saved_tribe.chieftain = request.user.profile
            saved_tribe.save()
            profile = saved_tribe.chieftain
            profile.tribes.add(saved_tribe)
            profile.save()
            return HttpResponseRedirect(reverse('app:tribe',args=(saved_tribe.id,)))
    else:
        form = TribeForm()
    context = {'form':form, 'action':'create'}
    return render(request,'app/create_tribe.html',context)

def update_tribe(request, tribe_id):
    
    tribe = get_object_or_404(Tribe, pk=tribe_id)
    if request.method == 'POST' and tribe.chieftain == request.user.profile:
        form = TribeForm(request.POST, instance = tribe)
        if form.is_valid():
            saved_tribe = form.save()
            return HttpResponseRedirect(reverse('app:tribe', args=(saved_tribe.id,)))
    else:
        form = TribeForm(instance=tribe)
        
    context = { 'form':form, 'action':'update', }
    return render(request, 'app/update_tribe.html', context)

def add_message(request,tribe_id):
    tribe= get_object_or_404(Tribe, pk=tribe_id)
    form = MessageForm(request.POST)
    if request.method == 'POST' and request.user.is_authenticated:  
        if form.is_valid():
            saved_message= form.save(commit=False)
            saved_message.user = request.user.profile
            saved_message.tribe = tribe
            saved_message.save()
            return HttpResponseRedirect(reverse('app:tribe', args=(saved_message.tribe.id,)))
        else:
            context = {'tribe':tribe,
                        'form':form}
            return render(request,'app/tribe.html',context)
    else:
        return HttpResponseRedirect(reverse('app:tribe',args=(tribe_id,)))
    


def create_playlist(request,tribe_id):
    tribe = Tribe.objects.filter(pk=tribe_id).first()
    if request.method == 'POST' and request.user.is_authenticated:
        form = PlaylistForm(request.POST)
        
        if form.is_valid():
            saved_playlist = form.save(commit=False)
            saved_playlist.creator = request.user.profile
            saved_playlist.tribe = tribe
            saved_playlist.save()
            return HttpResponseRedirect(reverse('app:tribe',args=(tribe.id,)))
    else:
        form = PlaylistForm()
    context = {'form':form, 'action':'create',}
    return render(request,'app/create_playlist.html',context)

def create_song(request,playlist_id):
    playlist = Playlist.objects.filter(pk=playlist_id).first()
    if request.method == 'POST' and request.user.is_authenticated:
        form = SongForm(request.POST)
        if form.is_valid():
            saved_song = form.save(commit=False)
            saved_song.creator = request.user.profile
            saved_song.playlist = playlist
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

def delete_playlist(request,playlist_id):
    playlist = Playlist.objects.filter(pk=playlist_id).first()
    tribe_id = playlist.tribe.id
    if request.user.profile == playlist.creator or request.user.profile == playlist.tribe.chieftain or request.user.is_superuser:
        playlist.delete()
    return HttpResponseRedirect(reverse('app:tribe',args=(tribe_id,)))

def delete_song(request,song_id):
    
    song = Song.objects.filter(pk=song_id).first()
    playlist = song.playlist
    tribe = playlist.tribe
    if request.user.profile == song.creator or request.user.profile == playlist.tribe.chieftain or request.user.is_superuser:
        song.delete()
    return HttpResponseRedirect(reverse('app:playlist',args=(tribe.id,playlist.id)))

def update_playlist(request,playlist_id):
    playlist = Playlist.objects.get(id=playlist_id)
    if request.method == 'POST' and playlist.tribe.chieftain == request.user.profile:
        form = PlaylistForm(request.POST,instance=playlist)
        if form.is_valid():
            saved_playlist = form.save()
            return HttpResponseRedirect(reverse('app:tribe', args=(saved_playlist.tribe.id,)))
    else:
        form = PlaylistForm(instance=playlist)
        
    context = { 'form':form, 'action':'update', }
    return render(request, 'app/update_playlist.html', context)

def leave(request,tribe_id):
    tribe = Tribe.objects.get(id=tribe_id)
    if request.method == 'POST' and request.user.is_authenticated:
        profile = request.user.profile
        profile.tribes.remove(tribe)
        
        return HttpResponseRedirect(reverse('app:tribe',args=(tribe_id,)))
    else:
        context = {"tribe":tribe}
        return render(request,"app/tribe.html",context)

def song(request,tribe_id,playlist_id,song_id):
    tribe = Tribe.objects.filter(pk=tribe_id).first()
    playlist = Playlist.objects.filter(pk=playlist_id,tribe=tribe).first()
    song = Song.objects.filter(playlist=playlist,pk=song_id).first()
    context={"playlist":playlist,
            "song":song,
            "tribe":tribe,
            }

    return render(request,"app/playlist.html",context)

def delete_message(request,tribe_id,message_id):
    tribe = Tribe.objects.filter(pk=tribe_id).first()
    message = Message.objects.filter(pk=message_id)
    if request.user.profile == tribe.chieftain or request.user.is_superuser:
        message.delete()
    return HttpResponseRedirect(reverse('app:tribe',args=(tribe.id,)))
   
def likebtn(request,song_id):
    song = Song.objects.filter(id=song_id).first()
    playlist = song.playlist
    tribe = playlist.tribe
    like = Like.objects.filter(song=song,user=request.user.profile).first()
    if request.method=='POST':
        if  is_member_of_tribe(request.user,tribe) or request.user.profile == tribe.chieftain:
            if like:
                like.delete()
            else:
                like_obj = Like(song=song,user=request.user.profile)
                like_obj.save()

    return HttpResponseRedirect(reverse('app:playlist',args=(tribe.id,playlist.id)))

def kick(request,tribe_id,user_id):
    tribe = Tribe.objects.get(id=tribe_id)
    user = User.objects.get(id=user_id)
    profile = user.profile
    if request.method == 'POST' and is_chieftain(profile,tribe):
        if request.user.profile == tribe.chieftain:
            pass
        else:
            profile.tribes.remove(tribe)       
        return HttpResponseRedirect(reverse('app:tribe',args=(tribe_id,)))
    else:
        context = {"tribe":tribe}
        return render(request,"app/tribe.html",context)

def add_comment(request,tribe_id,playlist_id,song_id):
    tribe= get_object_or_404(Tribe, pk=tribe_id)
    playlist =get_object_or_404(Playlist, pk=playlist_id)
    song = get_object_or_404(Song, pk=song_id)
    form = CommentForm(request.POST)
    if request.method == 'POST' and request.user.is_authenticated:  
        if form.is_valid():
            saved_comment= form.save(commit=False)
            saved_comment.user = request.user.profile
            saved_comment.song = song
            saved_comment.save()
            return HttpResponseRedirect(reverse('app:playlist', args=(tribe.id,playlist.id,)))
        else:
            context = {'playlist':playlist,
                'form':form}
            return render(request,'app/playlist.html',context)
    else:
        return HttpResponseRedirect(reverse('app:playlist',args=(tribe_id,playlist_id,)))