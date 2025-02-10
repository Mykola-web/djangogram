from symtable import Class

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.views.generic import TemplateView

from .models import Profile
from django.contrib.auth.hashers import make_password
from .forms import RegistrationForm, EditProfileForm, LoginForm, PostForm
from .services import send_activation_email, generate_activation_link
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator
from django.views import View
from django.db import IntegrityError

# def home(request):
#     return render(request, 'myapp/home.html')


class HomeView(TemplateView):
    template_name = 'myapp/home.html'


class RegisterView(View):
    def get(self, request):
        form = RegistrationForm()
        return render(request, 'myapp/registration.html', {'form': form})

    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = User.objects.create(username = username, email = email, is_active = False)
                user.set_password(password)
                user.save()

                activation_link = generate_activation_link(user)
                send_activation_email(user, activation_link)
                return render(request, 'myapp/sent_email.html')
            except IntegrityError:
                form.add_error('username', 'A user with this username is already registered')
                return render(request, 'myapp/registration.html', {'form':form})
        return render(request, 'myapp/registration.html', {'form': form})


class ActivateAccount(View):
    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return render(request, 'myapp/activation.html',
                          {'message': 'The activation link is invalid or expired.'})

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'myapp/activation.html',
                          {'message': '🎉Activation completed🎉'})
        else:
            return render(request, 'myapp/activation.html',
                          {'message': 'The activation link is invalid.'})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST,request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance = request.user.profile)

    return render(request, 'myapp/edit_profile.html', {'form': form})

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if not form.is_valid():
#             print('Form errors:', form.errors)
#             return render(request, 'myapp/login.html', {'form': form})
#
#         user = authenticate(
#             username = form.cleaned_data['username'],
#             password = form.cleaned_data['password']
#         )
#         if user is None:
#             print('Authentication failed:', user)
#             form.add_error(None, 'Invalid login credentials')
#             return render(request, 'myapp/login.html', {'form': form})
#
#         print('User authenticated:', user)
#         login(request, user)
#
#         # Вывод содержимого GET-запроса
#         print('Request GET:', request.GET)
#
#         next_url = request.POST.get('next') or request.GET.get('next')
#
#         return redirect(next_url if next_url else 'feed')
#
#     form = LoginForm()
#     return render(request, 'myapp/login.html', {'form': form})

class LoginView(View):
    def post(self, request):
        if request.user.is_authenticated:
            logout(request)

        form = LoginForm(request.POST)
        if not form.is_valid():
            print('Form errors:', form.errors)
            return render(request, 'myapp/login.html', {'form': form})

        user = authenticate(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password']
        )
        if user is None:
            print('Authentication failed:', user)
            form.add_error(None, 'Invalid login credentials')
            return render(request, 'myapp/login.html', {'form': form})

        print('User authenticated:', user)
        login(request, user)

        print('Request GET:', request.GET)

        next_url = request.POST.get('next') or request.GET.get('next')

        return redirect(next_url if next_url else 'feed')

    def get(self, request):
        if request.user.is_authenticated:
            logout(request)
            return redirect(request.GET.get('next', request.META.get('HTTP_REFERER', 'login')))
        form = LoginForm()
        return render(request, 'myapp/login.html', {'form': form})


class FeedView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'myapp/feed.html')


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'myapp/profile.html', {'user': request.user})


class PostingView(LoginRequiredMixin, View):
    def get(self, request):
        form = PostForm()
        return render(request, 'myapp/post.html', {'form': form})

    def post(self, request):
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit = False)
                post.author = request.user
                post.save()
            return redirect('profile')

# @login_required
# def feed(request):
#     return render(request, 'myapp/feed.html')
#
# @login_required
# def profile(request):
#     return render(request, 'myapp/profile_old.html')
#
# @login_required
# def make_post(request):
#     return render(request, 'myapp/post.html')