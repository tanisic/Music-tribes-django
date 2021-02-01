from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from .forms import ExtendedUserCreationForm, EditUserForm


class SignUpView(generic.CreateView):
    form_class=ExtendedUserCreationForm
    success_url= reverse_lazy('login')
    template_name = 'registration/signup.html'

# Create your views here.
def profile(request,user_id):
    user_profile = User.objects.filter(id=user_id).first()

def editprofile(request):
    if request.method == 'POST':
        form = EditUserForm(request.POST, instance=request.user)

        if form.is_valid():
            user_form = form.save()
            return redirect('app:index')
    else:
        form = EditUserForm(instance=request.user)
        context = {}
        # args.update(csrf(request))
        context['form'] = form
        return render(request, 'app/edituser.html', context)