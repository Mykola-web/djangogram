from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.HomeView.as_view() , name = 'home'),
    path('register', views.RegisterView.as_view(), name = 'register'),
    path('sent_email', views.RegisterView.as_view(), name = 'sent_email'),
    path('profile/edit', views.EditProfileView.as_view(), name = 'edit_profile'),
    path('feed', views.FeedView.as_view(), name = 'feed'),
    path('profile2', views.ProfileView.as_view(), name = 'profile'),
    path('post', views.PostingView.as_view(), name = 'post'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name = 'activate_account'),
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name = 'logout'),
    path('profile/<str:username>/', views.profileView.as_view(), name = 'profile'),
    path('profile/', views.profileView.as_view(), name = 'profile'),
    path('like_post/<int:post_id>/', views.LikePostView.as_view(), name = 'like_post'),
]
