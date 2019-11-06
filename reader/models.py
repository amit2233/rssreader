from django.utils import timezone
from django.db import models

# Create your models here.

class Source(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    site_url = models.CharField(max_length=255, blank=True, null=True)
    feed_url = models.CharField(max_length=255)
    etag = models.CharField(max_length=255, blank=True, null=True)
    last_modified = models.CharField(max_length=255, blank=True, null=True)


class Post(models.Model):
    source = models.ForeignKey(Source, on_delete=models.CASCADE, related_name='posts') 
    title = models.TextField(blank=True)  
    body = models.TextField()
    link = models.CharField(max_length=512, blank=True, null=True)
    guid = models.CharField(max_length=255, blank=True, null=True, db_index=True)
    created = models.DateTimeField(default=timezone.now)

