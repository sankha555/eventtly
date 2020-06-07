from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.http import HttpResponseRedirect
from events.models import Event, Registration
from users.models import Creator, CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from events.forms import EventRegistrationForm, TemplateForm, RegistrationForm, EventSearchForm
from allauth.socialaccount.models import SocialAccount
from django import forms
import hashlib
from django.utils.encoding import force_text
import random


def index(request):

    users = CustomUser.objects.all()
    events = Event.objects.all()
    regs = Registration.objects.all()

    #trending_events = Event.objects.filter(event.registrations >= 5)

    context = {
        'users' : users,
        'events' : events,
        'regs' : regs,
    }

    return render(request, 'events/index.htm', context)

@login_required
def dashboard(request):
    
    user = request.user
    emails = [u.email for u in CustomUser.objects.all()]
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

    def increase_page_visits(self):
        self.object.page_visits += 1
        self.object.save()

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'description', 'date', 'time', 'poster']
    template_name = 'events/event_form.htm'
    
    def get_success_url(self):
        return reverse('customise_reg_form', kwargs={'url': self.object.url})

    def form_valid(self, form):
        form.instance.creator = self.request.user.creator
        form.instance.url = self.request.user.email.split('@')[0] + '_' + form.cleaned_data['title'].replace(" ", "-")
        
        flag = 0
        while flag == 0:
            hash_attempt = force_text(str(hex(random.randint(0,16777215))))
            if Event.objects.filter(hashed_url = hash_attempt).exists():
                hash_attempt = force_text(random_hex(20))
                flag = 0
            else:
                flag = 1
                break

        form.instance.hashed_url = hash_attempt

        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['title', 'description', 'date', 'time', 'poster']
    template_name = 'events/event_form.htm'
    
    def get_success_url(self):
        return reverse('customise_reg_form', kwargs={'url': self.object.url})

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

def register_for_event(request, url):
    event = get_object_or_404(Event, url = url)
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
        event.page_visits += 1
        event.save()
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
def view_registrations(request, url):
    event = get_object_or_404(Event, url = url)
    if event.creator != request.user.creator:
        messages.error(request, "Unauthorised access!")
        return redirect('dashboard')
    else:
        regs = []
        for reg in Registration.objects.filter(event = event):
            regs.append(reg)

        return render(request, 'events/view_registrations.htm', {'regs': regs, 'event' : event})
    

@login_required
def customise_reg_form(request, url):
    event = get_object_or_404(Event, url = url)
    if request.method == "POST":
        form = TemplateForm(request.POST, instance = event)
        if form.is_valid():
            form.save()

            messages.success(request, "Registration Form Template Saved Successfully!")
            return redirect('dashboard')
    else:
        form = TemplateForm(instance = event)
    
    return render(request, 'events/customise_reg_form.htm', {'form' : form, 'event' : event})

def custom_register_for_event(request, url):
    event = get_object_or_404(Event, url = url)
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
    
def view_event(request, url):
    event = get_object_or_404(Event, url = url)
    return render(request, "events/event_detail.htm", {'object' : event})

def view_event_by_hashed_url(request, hashed_url):

    hashed = request.path_info
    hashed_url = hashed.strip('/')
    hashed_list = hashed_url.split('/')

    event = get_object_or_404(Event, hashed_url = hashed_list[-1])

    return redirect('view_event', event.url)
    
def search_events(request):
    if request.method == "POST":
        form = EventSearchForm(request.POST)
        
        if form.is_valid():

            #if form.cleaned_data.get('search_query') == None or form.cleaned_data.get('search_query') == " ":
            #    return redirect('index')
            
            search_query = form.cleaned_data.get('search_query')
            words_list = search_query.split()
            
            useless_words = ['of', 'at', 'the', 'with', 'a', 'an', 'on', 'in', 'by']

            for word in words_list:
                if word in useless_words:
                    words_list.pop(word)
            
            tags = words_list
            events = Event.objects.all().order_by('-date', '-registrations')
            
            top_priority_events = []
            low_priority_events = []

            relevance = []
    
            for event in events:
                tag_frequency = 0
                title_tags = event.title.split()
                desc_tags = event.description.split()
                desc = title_tags + desc_tags

                for tag in tags:
                    if tag in desc:
                        top_priority_events.append(event)
                        tag_frequency += 1
                relevance.append(tag_frequency)

            for event in events:
                if event in top_priority_events:
                    continue
                else:
                    low_priority_events.append(event)
            
            # Sorting events on basis of relevance
            if len(top_priority_events) != len(relevance):
                for i in range(len(top_priority_events) - len(relevance)):
                    relevance.append(max(relevance))

            for i in range(len(top_priority_events)):
                for j in range(i+1, len(top_priority_events)):
                    if relevance[i] < relevance[j]:
                        (top_priority_events[i], top_priority_events[j]) = (top_priority_events[j], top_priority_events[i])

            top_priority_events = list(dict.fromkeys(top_priority_events))

            queryset = {
                'top' : top_priority_events,
                'low' : low_priority_events,
                'query' : search_query
            }

            return render(request, 'events/search_results.htm', queryset)
        else:
            return redirect('index')
    else:
        form = EventSearchForm()
        

    return render(request, 'events/index.htm', {'form' : form})

