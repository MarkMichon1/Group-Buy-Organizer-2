from django.db import models

import uuid

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)


class Item(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    packing = models.SmallIntegerField()
    event = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='items')


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) #todo dont have ID, have url display slug
    name = models.CharField(max_length=100, null=False)
    description = models.CharField(max_length=200, default='No description added!')
    date_created = models.DateTimeField(auto_now_add=True)
    is_locked = models.BooleanField(default=False)
    is_closed = models.BooleanField(default=False)
    extra_charges = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='+')
    members = models.ManyToManyField(User, through='EventMembership')


class EventMembership(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_organizer = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    has_paid = models.BooleanField(default=False)


class CaseBuy(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='case_buys')
    quantity = models.SmallIntegerField(null=False)


class CaseSplit(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='case_splits')
    started_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created= models.DateTimeField(auto_now_add=True)
    is_complete = models.BooleanField(default=False)


class CasePieceCommit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    quantity = models.SmallIntegerField(null=False)
    case_split = models.ForeignKey(CaseSplit, on_delete=models.CASCADE, related_name='split_commits')