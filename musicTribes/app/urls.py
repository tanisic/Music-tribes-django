from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:tribe_id>/', views.tribe, name='tribe'),
]