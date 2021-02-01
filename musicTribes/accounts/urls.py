from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('sign-up', views.signup,name='signup'),
    path('<int:user_id>', views.profile, name="profile"),
    path('editprofile',views.editprofile, name="editprofile"),
    path('editprofile/changepassword',views.changepassword, name="changepassword"),
    path('editprofile/extendededit',views.extendededit, name="extendededit")
]
