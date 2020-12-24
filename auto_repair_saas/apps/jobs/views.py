from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView

from auto_repair_saas.apps.jobs.forms import NewJobForm
from auto_repair_saas.apps.jobs.models import Job


class JobsView(LoginRequiredMixin, View):
    form_class = NewJobForm
    template_name = 'jobs/index.html'

    def get(self, request, *args, **kwargs):
        jobs = Job.objects.all()
        form = self.form_class()
        return render(
            request, self.template_name, {'jobs': jobs, 'form': form}
        )

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                Job.objects.create(**form.cleaned_data)
                messages.success(request, 'Job created.')
                return HttpResponseRedirect(reverse('jobs'))
            except Exception as e:
                messages.error(request, str(e))
                return HttpResponseRedirect(reverse('jobs'))
        else:
            error = 'Form is invalid.'
            messages.error(request, error)
            return HttpResponseRedirect(reverse('jobs'))


class UpdateJobView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Job
    form = NewJobForm()
    fields = [*form.fields]
    success_url = reverse_lazy('jobs')
    success_message = 'Job updated.'


class DeleteJobView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('jobs')
    success_message = 'Job deleted.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteJobView, self).delete(request, *args, **kwargs)
