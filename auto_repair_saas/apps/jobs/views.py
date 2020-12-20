from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from auto_repair_saas.apps.jobs.forms import NewJobForm
from auto_repair_saas.apps.jobs.models import Job


class JobsView(LoginRequiredMixin, View):
    form_class = NewJobForm
    template_name = 'jobs/index.html'

    def get(self, request, *args, **kwargs):
        jobs = Job.objects.all()
        return render(request, self.template_name, {'jobs': jobs})


class NewJobView(LoginRequiredMixin, View):
    form_class = NewJobForm
    template_name = 'jobs/new.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                Job.objects.create(**form.cleaned_data)
                return HttpResponseRedirect(reverse('jobs'))
            except Exception as e:
                error = str(e)
                return render(
                    request, self.template_name, {
                        'form': form, 'error': error
                    }
                )
        else:
            error = 'Form is invalid.'
            return render(
                request, self.template_name, {
                    'form': form, 'error': error
                }
            )
