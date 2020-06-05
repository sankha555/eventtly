from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from PIL import Image
from django.conf import settings


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, is_admin=False, is_staff=False, is_active=True):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not name:
            raise ValueError("User must have a name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.name = name
        user.admin = is_admin
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, profile_picture, password=None, **extra_fields):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        if not name:
            raise ValueError("User must have a full name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.name = name
        user.admin = True
        user.staff = True
        user.active = is_active
        user.save(using=self._db)
        return user



class CustomUser(AbstractUser):
    username = None
    name = models.CharField(verbose_name = "Name", max_length=50)
    email = models.EmailField(verbose_name = "Email", max_length=254, unique = True)
    
    REQUIRED_FIELDS = []
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
