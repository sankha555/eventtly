from django import forms 
from users.models import Creator, CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreatorRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=50, required=True)
    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password']
        exclude = ('password1', 'password2')

class CreatorProfileForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = ['first_name', 'last_name', 'image']

