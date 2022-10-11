from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    image = models.ImageField(upload_to='images/profile/', blank=True, null=True)
    profile = models.TextField(blank=True, null=True)
