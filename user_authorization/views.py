# user_authorization/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .forms import RegistrationForm


def registration_view(request):
    if request.method == 'POST':
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'registration/registration.html', {'form': user_form, 'errors': user_form.errors})
    else:
        user_form = RegistrationForm()
    return render(request, 'registration/registration.html', {'form': user_form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = request.POST.get('remember_me')

            user = authenticate(request, username=username, password=password)

            if user is None:
                try:
                    user_email = User.objects.get(email=username)
                    user = authenticate(request, username=user_email.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user is not None:
                auth_login(request, user)
                if remember_me:
                    request.session.set_expiry(1209600)
                else:
                    request.session.set_expiry(0)
                return redirect(
                    'home')
            else:
                form.add_error(None, 'Invalid login credentials')
        else:
            form.add_error(None, 'Invalid login credentials')
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('welcome')

