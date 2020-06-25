from django.db import models

import uuid

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)


class Item(models.Model):
    name = None
    price = None
    packing = None
    category_id = None
    event = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='items')


class Event(models.Model):
    invite_key = models.UUIDField(default=uuid.uuid4)
    name = models.CharField()
    date_created = models.DateTimeField(auto_now_add=True)
    is_locked = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    extra_charges = models.DecimalField(max_digits=8, decimal_places=2)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


class EventUserAssociation(models.Model):
    pass


class Notification(models.Model):
    pass


class CaseBuy(models.Model):
    pass


class CaseSplit(models.Model):
    pass


class CasePieceCommit(models.Model):
    pass


class HasPaid(models.Model):
    pass