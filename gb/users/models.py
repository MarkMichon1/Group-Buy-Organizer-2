from django.db import models
from django.contrib.auth.models import AbstractUser

import uuid


class User(AbstractUser):
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


class PersonalMessage(models.Model):
    datetime_sent = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='sent_messages')
    recipient = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='received_messages')
    has_sender_deleted = models.BooleanField(default=False)
    has_recipient_deleted = models.BooleanField(default=False)
    is_opened = models.BooleanField(default=False)
    message_title = models.CharField(max_length=100)
    message_body = models.TextField(max_length=5000)

    class Meta:
        ordering = ('-datetime_sent',)