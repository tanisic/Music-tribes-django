from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic
from .forms import EditProfileForm, ExtendedUserCreationForm, EditUserForm,ChangePasswordForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login


#class SignUpView(generic.CreateView):
    #form_class=ExtendedUserCreationForm
    #success_url= reverse_lazy('login')
    #template_name = 'registration/signup.html'

def signup(request):
    if request.method == 'POST':
        user_form = ExtendedUserCreationForm(request.POST)
        profile_form=EditProfileForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            username = user_form.cleaned_data.get('username')
            raw_password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('app:index')
    else:
        user_form = ExtendedUserCreationForm()
    return render(request, 'registration/signup.html', {'form': user_form})
    
# Create your views here.
def profile(request,user_id):
    user_profile = User.objects.filter(id=user_id).first()

@login_required
@transaction.atomic
def editprofile(request):
    if request.method == 'POST':
        user_form = EditUserForm(request.POST, instance=request.user)
        profile_form=EditProfileForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return HttpResponseRedirect(reverse('app:index'))

        else: 
            return redirect('accounts:editprofile')

    else:
        user_form = EditUserForm(instance=request.user)
        profile_form = EditProfileForm(instance=request.user.profile)
        context = {}
        context['form']=user_form
        return render(request, 'app/edituser.html', context)

def extendededit(request):
    if request.method=='POST':
        form=EditProfileForm(request.POST, instance=request.user.profile)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('app:index'))   #change later to accounts:profile
        else:
            return HttpResponseRedirect(reverse('accounts:extendededit'))
    else:
        form=EditProfileForm(instance=request.user.profile)
        context = {}
        context['form']=form
        return render(request,'app/extendededit.html',context)



def changepassword(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, instance=request.user)

        if form.is_valid():
            user_form = form.save()
            return HttpResponseRedirect(reverse('app:index'))   #change later to accounts:profile

        else:
            return HttpResponseRedirect(reverse('accounts:changepassword'))

    else:
        form = ChangePasswordForm(instance=request.user)
        context = {}
        # args.update(csrf(request))
        context['form'] = form
        return render(request, 'app/changepassword.html', context)
