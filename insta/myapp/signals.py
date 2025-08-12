import os

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import ProfileModel, PostModel


@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        ProfileModel.objects.create(user = instance)
