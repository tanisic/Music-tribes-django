from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('sign-up', views.SignUpView.as_view(),name='signup'),
    path('<int:user_id>', views.profile, name="profile"),
    path('editprofile',views.editprofile, name="editprofile")
]
