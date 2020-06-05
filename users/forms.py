from django import forms 
from users.models import Creator, CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreatorRegistrationForm(UserCreationForm):
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['name', 'email']

class CreatorProfileForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = ['first_name', 'last_name', 'image']

class CustomRegistrationForm(forms.ModelForm):
    name = forms.EmailField(label = "Name")
    email = forms.EmailField(label = "Email")
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control','type':'password', 'name':'password'}),
        label="Password")
    username = forms.CharField(label = "username", initial = "user")

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password']   

    '''
    def __init__(self, *args, **kwargs): 
        super(CustomRegistrationForm, self).__init__(*args, **kwargs) 
        # remove username
        self.fields.pop('username')

    def save(self):
        random = self.cleaned_data.get('email').split('@')[0]
        self.instance.username = random
        return super(CustomRegistrationForm, self).save()
    '''
    

