from django.contrib.postgres.fields import JSONField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

import datetime

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(1500)
    image = None


class Manufacturer(models.Model):
    approved = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    approved_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000)
    year_formed = models.IntegerField(validators=[MinValueValidator(1900),
                                                  MaxValueValidator(datetime.datetime.now().year)])
    year_formed_approximate = models.BooleanField(default=False)
    year_ended = models.IntegerField(validators=[MinValueValidator(1900),
                                                  MaxValueValidator(datetime.datetime.now().year)])
    year_ended_approximate = models.BooleanField(default=False)
    images = None


class Firework(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    flagged = models.BooleanField(default=False)

    name = models.TextField(max_length=100)
    url_slug = models.SlugField()
    description = models.CharField()
    packing = None
    images = None
    attributes = JSONField(models.CharField)

    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name='fireworks')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='fireworks')

    comments = None


class Quality(models.Model):
    pass


class FireworkComment(models.Model):
    flagged = models.BooleanField(default=False)


class FireworkLike(models.Model):
    pass


class FireworkFavorite(models.Model):
    pass

'''Attributes:


'''