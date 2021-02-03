from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path('', views.index, name='index'),
    path('create_tribe', views.create_tribe, name='create_tribe'),
    path('create_playlist', views.create_playlist, name='create_playlist'),
    path('<int:tribe_id>/', views.tribe, name='tribe'),
    path('<int:tribe_id>/update_tribe/', views.update_tribe, name='update_tribe'),
    path('<int:tribe_id>/playlist/<int:playlist_id>', views.playlist, name='playlist'),
    path('playlist/<int:playlist_id>/create_song', views.create_song, name='create_song')
]