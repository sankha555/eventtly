from django import forms 
from users.models import Creator, CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreatorRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password1']

class CreatorProfileForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = ['first_name', 'last_name', 'image']

