from django.contrib import admin

from .models import Profile, PostModel, TagModel

admin.site.register(Profile)
admin.site.register(PostModel)
admin.site.register(TagModel)
