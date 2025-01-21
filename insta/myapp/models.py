from django.db import models
from django.contrib.auth.models import User
from django.db.models import ForeignKey


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name='profile')
    gender = models.TextField(blank = True, null = True)
    avatar = models.ImageField(upload_to = 'avatars/', default = 'avatars/default_avatar.jpg', blank = True)
    birth_date = models.DateField(blank = True, null = True)
    bio = models.TextField(blank = True, null = True)

    def __str__(self):
        return f"Profile of {self.user.username}"

