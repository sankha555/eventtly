from django.contrib import admin
from django.urls import path, include
from events.views import index, dashboard, EventListView, EventDetailView, EventCreateView, EventDeleteView, EventUpdateView, register_for_event, edit_registration, delete_registration, my_events, view_registrations, custom_register_for_event, customise_reg_form

urlpatterns = [
    path('', index, name = 'index'),
    path('dashboard/', dashboard, name = 'dashboard'),
    path('registrations/<int:pk>/delete', delete_registration, name = 'delete_registration'),
    path('my_events/', my_events, name = 'my_events'),   
    path('my_events/event/<int:pk>/registrations/', view_registrations, name = 'view_registrations'),
    path('events/', EventListView.as_view(), name = 'event_list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name = 'event_detail'),
    path('events/new', EventCreateView.as_view(), name = 'create_event'),
    path('events/<int:pk>/delete', EventDeleteView.as_view(), name = 'delete_event'),
    path('events/<int:pk>/update', EventUpdateView.as_view(), name = 'update_event'),
    #path('events/<int:pk>/register', register_for_event, name = 'register_for_event'),
    path('events/<int:pk>/register', custom_register_for_event, name = 'register_for_event'),
    path('events/<int:pk>/form', customise_reg_form, name = 'customise_reg_form'),

    #path('events/edit_registration/<int:pk>/', edit_registration, name = 'edit_registration'),
]
