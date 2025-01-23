from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth.hashers import make_password
from .forms import RegistrationForm, EditProfileForm
from .services import send_activation_email, generate_activation_link
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from django.contrib.auth.tokens import default_token_generator

def home(request):
    return render(request, 'myapp/home.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            user = User.objects.create(username = username, email = email, password = password, is_active = False)
            user.save()

            activation_link = generate_activation_link(user)
            send_activation_email(user, activation_link)

            return render(request, 'myapp/sent_email.html')
    else:
        form = RegistrationForm()

    return render(request, 'myapp/registration.html', {form:form})


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'myapp/activation.html', {'message' : '🎉Activation completed🎉'})
    else:
        return render(request, 'myapp/activation.html', {'message' : 'The activation link is invalid.'})


def profile_edit(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        print("method_post")
        if form.is_valid():
            print("form_valid")
            user = request.user
            first_name = form.cleaned_data['username']
            last_name = form.cleaned_data['email']
            gender = form.cleaned_data['gender']
            avatar = form.cleaned_data['avatar']
            bio = form.cleaned_data['bio']
            birth_date = form.cleaned_data['birth_date']
            print("data received")
            profile_change = Profile.objects.create(
                first_name = first_name,
                last_name = last_name,
                gender = gender,
                avatar = avatar,
                bio = bio,
                birth_date = birth_date
            )
            user.save()
            print("Данные сохранены в базе данных")
            return render(request, 'myapp/home.html')
        else:
            print(form.errors)  # Печать ошибок в консоль
            return render(request, 'myapp/profile_edit.html', {'form': form})
    else:
        return render(request, 'myapp/profile_edit.html')


def login(request):
    return render(request, 'myapp/login.html')


def feed(request):
    return render(request, 'myapp/feed.html')


def profile(request):
    return render(request, 'myapp/profile.html')


def make_post(request):
    return render(request, 'myapp/post.html')