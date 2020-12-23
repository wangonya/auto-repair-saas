from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .forms import RegistrationForm, LoginForm
from .models import User


class LoginUserView(LoginView):
    template_name = 'auth/login.html'
    authentication_form = LoginForm
    redirect_authenticated_user = True


class RegisterUserView(View):
    form_class = RegistrationForm
    template_name = 'auth/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                User.objects.create_user(
                    form.cleaned_data['name'],
                    form.cleaned_data['email'],
                    form.cleaned_data['password']
                )
                success = 'Account registered successfully. ' \
                          'A verification email has been sent to ' \
                          f"{form.cleaned_data['email']}."
                messages.success(request, success)
                return HttpResponseRedirect(reverse('login'))
            except IntegrityError:
                error = 'An account with that email already exists.'
                return render(
                    request, self.template_name, {
                        'form': form, 'error': error
                    }
                )
            except Exception as e:
                error = str(e)
                messages.error(request, error)
                return HttpResponseRedirect(reverse('register'))
