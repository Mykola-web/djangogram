from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('signin', views.signin),
    path('signup', views.signup),
    path('profile/edit', views.profile_edit),
    path('feed', views.feed),
    path('profile', views.profile),
    path('post', views.make_post),
]
