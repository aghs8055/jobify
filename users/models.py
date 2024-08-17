import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser


def get_logo_upload_path(_, filename):
    return f"logos/{uuid.uuid4()}.{filename.split('.')[-1]}"


class User(AbstractUser):
    def __str__(self):
        return self.get_full_name()


class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    website = models.URLField(null=True, blank=True)
    address = models.CharField(max_length=255)
    logo = models.ImageField(upload_to=get_logo_upload_path, null=True, blank=True)
    description = models.TextField()

    def __str__(self):
        return self.company_name
