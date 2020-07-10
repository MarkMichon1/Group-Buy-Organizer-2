from django.db import models

# Create your models here.
class Instance(models.Model):
    service_initialized = models.BooleanField(default=False)