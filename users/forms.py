from django import forms 
from users.models import Creator, CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreatorRegistrationForm(UserCreationForm):
    
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ['name', 'email']

        def __init__(self, *args, **kwargs):
           super(CreatorRegistrationForm, self).__init__(*args, **kwargs)
           del self.fields['password2']
            

class CreatorProfileForm(forms.ModelForm):
    class Meta:
        model = Creator
        fields = ['first_name', 'last_name', 'image']

class CustomRegistrationForm(forms.Form):
    name = forms.CharField(max_length = 50, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=False)

    

