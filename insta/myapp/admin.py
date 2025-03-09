from django.contrib import admin

from .models import ProfileModel, PostModel, TagModel

admin.site.register(ProfileModel)
admin.site.register(PostModel)
admin.site.register(TagModel)
