from django.contrib import admin
from users.models import Creator, CustomUser

admin.site.register([CustomUser, Creator])

# Register your models here.
