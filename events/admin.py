from django.contrib import admin
from events.models import Event, Registration

admin.site.register([Event, Registration])

# Register your models here.
