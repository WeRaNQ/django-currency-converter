from django.shortcuts import render,redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages




def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form":form
    }
    if form.is_valid():
        form.save()
        return redirect('/login')
    return render(request,"register.html", context)

def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request,email=email, password=password)
        if user is not None:
            login(request,user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if url_has_allowed_host_and_scheme(redirect_path, request.get_host()):
                return redirect(redirect_path)

            else:
                return redirect('/')
        else:
            messages.error(request, "Неверный email или пароль")
    return render(request,"login.html",context)

def home_page(request):
    if request.user == AnonymousUser():
        return render(request, 'main.html')
    return render(request, 'main.html', {'name': request.user.nickname})

@login_required
def profile_page(request):
    context = {
        'name': request.user.nickname,
        'email': request.user.email,
        'role': request.user.role,
    }
    return render(request, 'profile.html', context)

def logout_page(request):
    logout(request)
    return redirect('/')



