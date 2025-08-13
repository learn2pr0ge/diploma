from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    client_name = models.CharField(max_length=255, blank=True)
    service_organization = models.CharField(max_length=255, blank=True)
    management = models.BooleanField(default=False)

    def __str__(self):
        return self.client_name

# Create your models here.
