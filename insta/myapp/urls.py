from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('profile/edit', views.profile_edit, name='profile_edit'),
    path('feed', views.feed, name='feed'),
    path('profile', views.profile, name='profile'),
    path('post', views.make_post, name='post'),
]
