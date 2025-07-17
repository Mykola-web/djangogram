from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.HomeView.as_view() , name = 'home'),
    path('register', views.RegisterView.as_view(), name = 'register'),
    path('sent_email', views.RegisterView.as_view(), name = 'sent_email'),
    path('profile/edit', views.EditProfileView.as_view(), name = 'edit_profile'),
    path('feed/', views.FeedView.as_view(), name = 'feed'),
    path('sub_feed/', views.SubFeedView.as_view(), name='sub_feed'),
    path('post', views.PostingView.as_view(), name = 'post'),
    path('activate/<uidb64>/<token>/', views.ActivateAccount.as_view(), name = 'activate_account'),
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name = 'logout'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name = 'profile'),
    path('profile/', views.ProfileView.as_view(), name = 'profile'),
    path('like_post/<int:post_id>/', views.LikePostView.as_view(), name = 'like_post'),
    #password reset logic:
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='myapp/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='myapp/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='myapp/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='myapp/password_reset_complete.html'),
         name='password_reset_complete'),
    #google authorization logic:
    path('accounts/', include('allauth.urls')),
]
