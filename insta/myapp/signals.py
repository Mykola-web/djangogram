import os

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ProfileModel, PostModel


@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user = instance)

@receiver(pre_delete, sender = PostModel)
def delete_image(sender, instance, **kwargs):
    if instance.image:
        image_path = instance.image.path
        if os.path.isfile(image_path):
            print(f"Deleting image at {image_path}")
            os.remove(image_path)
        else:
            print(f"Image not found at {image_path}")