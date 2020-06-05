from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.http import HttpResponseRedirect
from events.models import Event, Registration
from users.models import Creator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from events.forms import EventRegistrationForm, TemplateForm, RegistrationForm
from allauth.socialaccount.models import SocialAccount
from django import forms

def index(request):
    return render(request, 'events/index.htm')

@login_required
def dashboard(request):
    
    user = request.user
    emails = [u.email for u in User.objects.all()]
    try:
        creator = Creator.objects.get(user = user)
    except:
        new_creator = Creator.objects.create(
            user = user,
            first_name = user.first_name,
            last_name = user.last_name,
        )
        new_creator.save()

    events = [ event for event in Event.objects.filter(creator = request.user.creator) ]

    context = {
        'user' : user,
        'creator' : user.creator,
        'events' : events,
    }
    return render(request, 'events/dashboard.htm', context)

class EventListView(ListView):
    model = Event
    template_name = 'events/event_list.htm'
    context_object_name = 'events'
    ordering = ['-date']

class EventDetailView(DetailView):
    model = Event
    template_name = 'events/event_detail.htm'
    context_object_name = 'event'

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'description', 'date', 'time', 'poster']
    template_name = 'events/event_form.htm'
    
    def get_success_url(self):
        return reverse('customise_reg_form',args=(self.object.id))

    def form_valid(self, form):
        form.instance.creator = self.request.user.creator
        form.instance.url = self.request.user.username + form.cleaned_data['title']
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['title', 'description', 'date', 'time', 'poster']
    template_name = 'events/event_form.htm'
    success_url = 'events/<int:pk>/form'

    def form_valid(self, form):
        form.instance.creator = self.request.user.creator
        return super().form_valid(form)

    def test_func(self):
        event = self.get_object()
        if self.request.user.creator == event.creator:
            return True
        return False

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = 'dashboard/'

    def test_func(self):
        event = self.get_object()
        if self.request.user.creator == event.creator:
            return True
        return False

def register_for_event(request, pk):
    event = get_object_or_404(Event, pk = pk)
    #new_reg = Registration.objects.create(event = event)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.event = event
            form.save()
            event.registrations += 1
            event.save()

            messages.success(request, "Registration for Event Successful!")
            return redirect('index')
    else :
        form = EventRegistrationForm()
    return render(request, 'events/register_for_event.htm', {'form' : form, 'event' : event})


def edit_registration(request, pk):
    reg = get_object_or_404(Registration, pk = pk)
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST, request.FILES, instance = reg)
        if form.is_valid():
            form.save()
            return redirect('registration_details')
    else :
        form = EventRegistrationForm(instance = reg)
    return render(request, 'events/register_for_event.htm', {'form' : form})


@login_required
def delete_registration(request, pk):
    reg = get_object_or_404(Registration, pk = pk)
    if reg.event.creator != request.user.creator:
        messages.error(request, "Unauthorised access!")
        return redirect('dashboard')
    else:
        Registration.objects.delete(reg)
        reg.event.registrations -= 1
        reg.event.save()
        messages.error(request, "Registration cancelled!")
        return redirect('dashboard')

@login_required
def my_events(request):
    return redirect('dashboard')

@login_required
def view_registrations(request, pk):
    event = get_object_or_404(Event, pk = pk)
    if event.creator != request.user.creator:
        messages.error(request, "Unauthorised access!")
        return redirect('dashboard')
    else:
        regs = []
        for reg in Registration.objects.filter(event = event):
            regs.append(reg)

        return render(request, 'events/view_registrations.htm', {'regs': regs, 'event' : event})
    

@login_required
def customise_reg_form(request, pk):
    event = get_object_or_404(Event, pk = pk)
    if request.method == "POST":
        form = TemplateForm(request.POST, instance = event)
        if form.is_valid():
            form.save()

            messages.success(request, "Registration Form Template Saved Successfully!")
            return redirect('dashboard')
    else:
        form = TemplateForm(instance = event)
    
    return render(request, 'events/customise_reg_form.htm', {'form' : form, 'event' : event})

def custom_register_for_event(request, pk):
    event = get_object_or_404(Event, pk = pk)
    if request.method == "POST":
        form = EventRegistrationForm(
            request.POST, 
            request.FILES
        )
        if form.is_valid():
            
            form.instance.event = event
            form.save()

            event.registrations += 1
            event.save()

            messages.success(request, "Registration for Event Successful!")
            return redirect('index')
        else:
            messages.error(request, "Please fill the fields properly")
    else:
        form = EventRegistrationForm()
    
    return render(request, 'events/register_for_event.htm', {'form' : form, 'event' : event})
    

    
    
# Create your views here.
