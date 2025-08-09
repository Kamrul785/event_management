from django.db import models
from django.conf import settings
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    category = models.ForeignKey(
        'Category',
        on_delete=models.DO_NOTHING,
        related_name='events'
    )
    asset = models.ImageField(
        upload_to='event_asset', 
        blank=True, 
        null=True, 
        default='event_asset/default_img.png'
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='event',
        blank=True,
        null=True
    )
    
    def __str__(self):
        return self.name

