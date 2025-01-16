from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request, 'myapp/home.html')


def signin(request):
    return render(request, 'myapp/about.html')


def signup(request):
    return render(request, 'myapp/about.html')


def profile_edit(request):
    return render(request, 'myapp/about.html')


def feed(request):
    return render(request, 'myapp/about.html')


def profile(request):
    return render(request, 'myapp/about.html')


def make_post(request):
    return render(request, 'myapp/about.html')