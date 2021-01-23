from django.urls import path
from . import views

app_name = 'accounts'
urlpatterns = [
    path('<int:user_id>', views.profile, name="profile"),
]
