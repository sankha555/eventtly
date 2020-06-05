from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image
from django.conf import settings


class CustomUser(AbstractUser):
    username = None
    name = models.CharField(verbose_name = "Name", max_length=50)
    email = models.EmailField(verbose_name = "Email", max_length=254, unique = True)
    
    
    USERNAME_FIELD = 'email'


class Creator(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name = "First Name", max_length=50)
    last_name = models.CharField(verbose_name = "Last Name", max_length=50)
    image = models.ImageField(upload_to="media/user_pics", default="default_user.png")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height>400 or img.width > 400:
            output_size = (400, 400)
            img.thumbnail(output_size)
            img.save(self.image.path)

# Create your models here.
