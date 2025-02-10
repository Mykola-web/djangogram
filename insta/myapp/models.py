import logging
import os

from django.db import models
from django.contrib.auth.models import User
from django.db.models import ForeignKey
from django.dispatch import receiver

logger = logging.getLogger(__name__)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, default='male')
    avatar = models.ImageField(upload_to = 'avatars/', default = 'avatars/default_avatar.png', blank = True)
    birth_date = models.DateField(blank = True, null = True)
    bio = models.TextField(blank = True, null = True)

    def __str__(self):
        return f"Profile of {self.user.username}"

class PostModel(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'post')
    text = models.TextField(blank=True)
    image = models.ImageField(upload_to = 'posts/', blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)

    def clean(self):
        if not self.text and not self.image:
            logger.warning(f"User {self.author} attempted to create an empty post.")
            print("❌ Error: Cannot create an empty post!")
            # No `raise ValidationError()` to avoid crashing the page

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (f"Post by {self.author.username}:"
                f" {'Text and image post' if self.text and self.image else 'Simple post'}")