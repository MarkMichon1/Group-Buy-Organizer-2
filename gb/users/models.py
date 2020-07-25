from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    night_mode_enabled = models.BooleanField(default=False, blank=False)
    display_explanations = models.BooleanField(default=True)
    # timezone = future feature

    def __str__(self):
        return self.username


    def toggle_night_mode(self):
        self.night_mode_enabled = not self.night_mode_enabled
        self.save()

    def toggle_explanations(self):
        self.display_explanations = not self.display_explanations
        self.save()

    def send_event_status_email(self, status):
        pass #future feature

    class Meta:
        ordering = ('username',)