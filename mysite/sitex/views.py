from django.shortcuts import render,redirect
from .forms import RegisterForm, LoginForm
from django.contrib.auth import authenticate, login
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .forms import ConvertForm
from .models import UserLastCurrency
import requests




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
    if not request.user.is_authenticated:
        return render(request, 'main.html')

    form = ConvertForm(request.POST or None)
    context = {'form': form, 'name': request.user.nickname}

    if form.is_valid():
        currency1 = request.POST.get('fcurrency')
        currency2 = request.POST.get('scurrency')
        amount = request.POST.get('amount')

        if int(amount) > 0:
            url = f"https://api.apilayer.com/currency_data/convert?to={currency2}&from={currency1}&amount={amount}"
            headers = {"apikey": settings.API_KEY}
            response = requests.get(url, headers=headers).json()

            if 'result' in response:
                result = response['result']
                context['result'] = result

                UserLastCurrency.objects.update_or_create(
                    user_id=request.user.id,
                    defaults={
                        'currencyfrom': currency1,
                        'currencyto': currency2,
                        'amount': amount,
                    }
                )

    return render(request, 'main.html', context)



@login_required
def profile_page(request):
    context = {
        'name': request.user.nickname,
        'email': request.user.email,
        'role': request.user.role,
    }
    try:
        info = UserLastCurrency.objects.get(user=request.user)
        context['fcurrency'] = info.currencyfrom
        context['tcurrency'] = info.currencyto
        context['amount'] = info.amount
    except UserLastCurrency.DoesNotExist:
        pass
    return render(request, 'profile.html', context)

def logout_page(request):
    logout(request)
    return redirect('/')



