from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .forms import RegistrationForm

def home(request):
    return render(request, 'myapp/home.html')


def login(request):
    return render(request, 'myapp/login.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            print(first_name, email, last_name, password)

            # User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)

            return redirect('home')  # Перенаправляем на страницу успеха
    else:
        form = RegistrationForm()

    return render(request, 'myapp/Registration.html', {form:form})


def profile_edit(request):
    return render(request, 'myapp/profile_edit.html')


def feed(request):
    return render(request, 'myapp/feed.html')


def profile(request):
    return render(request, 'myapp/profile.html')


def make_post(request):
    return render(request, 'myapp/post.html')