from django.shortcuts import render, get_object_or_404, redirect
from users.models import Creator
from users.forms import CreatorRegistrationForm,CreatorProfileForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from allauth.socialaccount.models import SocialAccount


def register(request):
    if request.method == 'POST':
        form = CreatorRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            messages.success(request, f'Complete Your Profile!')
            
            # logging the user in
            user = authenticate(username=username, password=form.cleaned_data['password1'])
            login(request, user)

            new_creator = Creator.objects.create(
                user = request.user,
                first_name = name.split('')[0],
                last_name = name.split('')[-1],
            )
            new_creator.save()
            
            return redirect('profile')
    else :
        form = CreatorRegistrationForm()
    return render(request, 'users/register.htm', {'form' : form})

@login_required
def profile(request):
    profile = get_object_or_404(Creator, user = request.user)
    if request.method == 'POST':
        form = CreatorProfileForm(request.POST, instance = request.user.creator)

        if form.is_valid():
            form.save()

    else:
        form = CreatorProfileForm(instance=request.user.creator)

    context = {
        'form' : form
    }
    return render(request, 'users/profile.htm', context)

# Create your views here.
