import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    night_mode_enabled = models.BooleanField(default=False, blank=False)
    display_explanations = models.BooleanField(default=True)

    def __str__(self):
        return self.username

    def send_activation_email(self):
        pass

    def toggle_night_mode(self):
        self.night_mode_enabled = not self.night_mode_enabled
        self.save()

    def send_event_status_email(self, status):
        pass