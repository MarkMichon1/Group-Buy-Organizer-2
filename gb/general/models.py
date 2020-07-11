from django.db import models

from users.models import User

# Create your models here.
class Instance(models.Model):
    service_initialized = models.BooleanField(default=False)


class BlogPost(models.Model):
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='blog_posts')
    date_created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)
    content = models.TextField()