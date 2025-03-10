import logging

from django.db import models
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)

class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, related_name = 'profile')
    first_name = models.CharField(max_length = 20, blank = True)
    last_name = models.CharField(max_length = 20, blank = True)
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    gender = models.CharField(max_length = 6, choices = GENDER_CHOICES, default = 'male')
    avatar = models.ImageField(upload_to = 'avatars/', default = 'avatars/default_avatar.png', blank = True)
    birth_date = models.DateField(blank = True, null = True)
    bio = models.TextField(blank = True, null = True)

    objects = models.Manager()

    def __str__(self):
        return f"Profile of {self.user.username}"

    class Meta:
        app_label = 'myapp'


class PostModel(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'post')
    text = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add = True)
    tags = models.ManyToManyField('TagModel', related_name = 'posts', blank = True)
    likes = models.ManyToManyField(User, related_name = 'liked_posts', blank = True)

    objects = models.Manager()

    def clean(self):
        if not self.text and not self.images:
            logger.warning(f"User {self.author} attempted to create an empty post.")
            print("❌ Error: Cannot create an empty post!")
            # No `raise ValidationError()` to avoid crashing the page

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return (f"Post by {self.author.username}:"
                f" {'Text and image post' if self.text and self.images else 'Simple post'}")


class TagModel(models.Model):
    name = models.CharField(max_length = 50, unique = True)

    def __str__(self):
        return f'{self.name}'

class PostImage(models.Model):
    post = models.ForeignKey(PostModel, on_delete = models.CASCADE, related_name = 'images')
    image = models.ImageField(upload_to = 'post_images/')

    def __str__(self):
        return f'Image for {self.post.author.username}' if self.post else "Orphaned Image"
