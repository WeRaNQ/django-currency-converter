from django.shortcuts import render
from .forms import RegisterForm, LoginForm
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def register_page(request):
    form = RegisterForm()
    return render(request, 'register.html', {'form': form})


def login_page(request):
    form = LoginForm()
    return render(request, 'login.html', {'form': form})
