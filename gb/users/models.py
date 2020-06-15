from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    night_mode_enabled = models.BooleanField(default=False, blank=False)