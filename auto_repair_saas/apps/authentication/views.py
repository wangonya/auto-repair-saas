import logging

from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetView, \
    PasswordResetConfirmView as PasswordResetConfirm, \
    PasswordResetDoneView as PasswordResetDone, \
    PasswordResetCompleteView as PasswordResetComplete
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from .forms import RegistrationForm, LoginForm, PasswordResetRequestForm, \
    PasswordResetConfirmForm
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
                    form.cleaned_data['password2']
                )
                success = 'Account registered successfully.'
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
                logging.error(e)
                error = 'Sorry, something went wrong. Please try again later.'
                messages.error(request, error)
                return HttpResponseRedirect(reverse('register'))
        else:
            return render(
                request, self.template_name, {
                    'form': form
                }
            )


class PasswordResetRequestView(PasswordResetView):
    form_class = PasswordResetRequestForm
    template_name = 'auth/password_reset_request.html'
    subject_template_name = 'auth/password_reset_subject.txt'
    email_template_name = 'auth/password_reset_email.html'


class PasswordResetConfirmView(PasswordResetConfirm):
    form_class = PasswordResetConfirmForm
    template_name = 'auth/password_reset_confirm.html'


class PasswordResetDoneView(PasswordResetDone):
    template_name = 'auth/password_reset_done.html'


class PasswordResetCompleteView(PasswordResetComplete):
    template_name = 'auth/password_reset_complete.html'
