from django.db import models
from users.models import Creator
from PIL import Image
import datetime
import math

class Event(models.Model):
    creator = models.ForeignKey(Creator, on_delete=models.CASCADE)
    title = models.CharField(verbose_name = "Event Name", max_length=50)
    description = models.TextField(verbose_name = "Event Description", max_length=400)
    created_on = models.DateTimeField(auto_now=True)    # announcement date
    date = models.DateField(verbose_name = "Event Date", auto_now=False)
    time = models.TimeField(verbose_name = "Event Time", auto_now=False)
    last_reg_date = models.DateTimeField(auto_now=True)
    
    poster = models.ImageField(upload_to="posters", default="default_poster.png")
    url = models.CharField(max_length=50, null = True, blank = True)
    hashed_url = models.CharField(max_length=8, null = True, blank = True)

    # Form Fields
    req_name = models.BooleanField(verbose_name="Name", default = True)
    req_phone = models.BooleanField(verbose_name="Phone", default = True)
    req_email = models.BooleanField(verbose_name="Email", default = True)
    req_college = models.BooleanField(verbose_name="College", default = True)
    req_image = models.BooleanField(verbose_name="Image", default = False)

    # Analytics
    registrations = models.IntegerField(default = 0)
    page_visits = models.IntegerField(default = 0)

    def get_popularity_index(self):
        time_diff = datetime.datetime.now() - self.created_on 
        hours_active = math.floor(divmod(difference.days * 24 + difference.minutes, 60)) + 0.5
        index = self.page_visits / hours_active

        return index

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.poster.path)

        if img.height>800 or img.width > 1000:
            output_size = (800, 1000)
            img.thumbnail(output_size)
            img.save(self.poster.path)

class Registration(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(verbose_name = "Participant Name", max_length=50, default = " ")
    phone = models.CharField(verbose_name = "Participant Mobile", max_length=14, default = " ")
    email = models.EmailField(verbose_name = "Participant Email", max_length=100, default = " ")
    college = models.CharField(verbose_name = "Participant College", max_length=100, default = " ")
    image = models.ImageField(upload_to="participants", default="default_user.png")
    date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height>800 or img.width > 1000:
            output_size = (800, 1000)
            img.thumbnail(output_size)
            img.save(self.image.path)

'''
class Search(models.Model):
    search_query = models.CharField(max_length=250)
'''
# Create your models here.
