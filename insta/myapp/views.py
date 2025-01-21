from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'myapp/home.html')


def login(request):
    return render(request, 'myapp/login.html')


def register(request):
    return render(request, 'myapp/Registration.html')


def profile_edit(request):
    return render(request, 'myapp/profile_edit.html')


def feed(request):
    return render(request, 'myapp/feed.html')


def profile(request):
    return render(request, 'myapp/profile.html')


def make_post(request):
    return render(request, 'myapp/post.html')