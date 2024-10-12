from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    photo = models.FileField(null=True,blank=True,upload_to='technicians')
    is_technician = models.BooleanField(default=True)
    mobile = models.CharField(max_length=20)

    def __str__(self):
        return self.username