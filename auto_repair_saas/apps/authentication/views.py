from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import RegistrationForm, LoginForm
from .models import User


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            try:
                User.objects.get(email=form.cleaned_data['email'])
                error = 'An account with that email already exists.'
                return render(
                    request, 'auth/register.html', {
                        'form': form, 'error': error
                    }
                )
            except ObjectDoesNotExist:
                User.objects.create_user(
                    form.cleaned_data['name'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                print(f'Ok! Send verification email.')
    else:
        form = RegistrationForm()
    return render(request, 'auth/register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['email'],
                                password=form.cleaned_data['password'])
            if user is not None:
                return HttpResponseRedirect('/')
            else:
                error = 'Invalid email / password.'
                return render(
                    request, 'auth/login.html', {
                        'form': form, 'error': error
                    }
                )
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})
