from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import User

from .forms import RegistrationForm, LoginForm


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
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
                print('invalid credentials')
    else:
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})
