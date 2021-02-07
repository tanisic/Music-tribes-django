from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path('', views.index, name='index'),
    path('create_tribe', views.create_tribe, name='create_tribe'),
    path('<int:tribe_id>/', views.tribe, name='tribe'),
    path('<int:tribe_id>/join', views.join, name='join'),
    path('<int:tribe_id>/leave', views.leave, name='leave'),
    path('<int:tribe_id>/create_playlist', views.create_playlist, name='create_playlist'),
    path('<int:tribe_id>/update_tribe/', views.update_tribe, name='update_tribe'),
    path('<int:tribe_id>/add_message', views.add_message, name='add_message'),
    path('<int:tribe_id>/delete_message/<int:message_id>', views.delete_message, name='delete_message'),
    path('<int:tribe_id>/playlist/<int:playlist_id>', views.playlist, name='playlist'),
    path('<int:song_id>/delete_song', views.delete_song, name='delete_song'),
    path('<int:song_id>/like', views.likebtn, name='likebtn'),
    path('playlist/<int:playlist_id>/create_song', views.create_song, name='create_song'),
    path('playlist/<int:playlist_id>/update_playlist', views.update_playlist, name='update_playlist'),
    path('playlist/<int:playlist_id>/delete_playlist', views.delete_playlist, name='delete_playlist'),
]