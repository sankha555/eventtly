from django import forms 
from events.models import Event, Registration

class EventRegistrationForm(forms.ModelForm):

    name = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    email = forms.CharField(required=False)
    college = forms.CharField(required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Registration
        fields = ['name', 'phone', 'email', 'college', 'image']

class TemplateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['req_name', 'req_phone', 'req_email', 'req_college', 'req_image']

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['name', 'phone', 'email', 'college', 'image']

  
class EventSearchForm(forms.Form):
    search_query = forms.CharField(max_length=250, required=True)