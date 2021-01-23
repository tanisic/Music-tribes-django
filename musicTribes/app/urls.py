from django.urls import path

from . import views

app_name = "app"
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:tribe_id>/', views.tribe, name='tribe'),
    path('<int:tribe_id>/playlist/<int:playlist_id>', views.playlist, name='playlist')
]