from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    profile_image = models.ImageField(
        upload_to='profile_image',
        blank=True,
        default='profile_image/default.png'
    )
    phone_number = models.CharField(
        max_length=17,
        validators=[
            RegexValidator(
                regex=r'^\+?1?\d{9,15}$',
                message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
            )    
        ],
        blank=True
    )
    
    def __str__(self):
        return self.username
    