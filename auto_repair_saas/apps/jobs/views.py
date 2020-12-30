from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView

from auto_repair_saas.apps.jobs.forms import NewJobForm, RegisterPaymentForm
from auto_repair_saas.apps.jobs.models import Job
from auto_repair_saas.apps.utils.search import SearchForm


class JobsView(LoginRequiredMixin, View):
    form_class = NewJobForm
    search_form = SearchForm
    register_payment_form = RegisterPaymentForm
    template_name = 'jobs/index.html'

    def get(self, request, *args, **kwargs):
        jobs = Job.objects.all()
        estimates = jobs.exclude(status__in=('in_progress', 'done'))
        in_progress = jobs.filter(status='in_progress')
        done = jobs.filter(status='done')
        form = self.form_class()
        search_form = self.search_form()
        register_payment_form = self.register_payment_form()
        context = {
            'estimates': estimates,
            'estimates_count': estimates.count(),
            'in_progress': in_progress,
            'in_progress_count': in_progress.count(),
            'done': done,
            'done_count': done.count(),
            'form': form,
            'search_form': search_form,
            'register_payment_form': register_payment_form,
        }
        return render(
            request, self.template_name, context
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
            try:
                form_error = form.non_field_errors().get_json_data()[0].get(
                    'message')
                error = f"Invalid input. {form_error}"
            except IndexError:
                pass
            messages.error(request, error)
            return HttpResponseRedirect(reverse('jobs'))


class JobsSearchView(LoginRequiredMixin, View):
    search_form_class = SearchForm
    job_form_class = NewJobForm
    template_name = 'jobs/index.html'

    def get(self, request, *args, **kwargs):
        search_form = self.search_form_class(request.GET)
        job_form = self.job_form_class()

        if not search_form.is_valid():
            HttpResponseRedirect(reverse('jobs'))

        if search_form.cleaned_data.get('q') == '':
            jobs = Job.objects.all()
        else:
            jobs = Job.objects.annotate(
                search=SearchVector('client__name', 'vehicle__number_plate'),
            ).filter(search=search_form.cleaned_data.get('q'))

        estimates = jobs.exclude(status__in=('in_progress', 'done'))
        in_progress = jobs.filter(status='in_progress')
        done = jobs.filter(status='done')

        context = {
            'estimates': estimates,
            'estimates_count': estimates.count(),
            'in_progress': in_progress,
            'in_progress_count': in_progress.count(),
            'done': done,
            'done_count': done.count(),
            'form': job_form,
            'search_form': search_form
        }
        return render(
            request, self.template_name, context
        )


class UpdateJobView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Job
    form = NewJobForm()
    fields = [*form.fields]
    success_url = reverse_lazy('jobs')
    success_message = 'Job updated.'


class RegisterJobPaymentView(
    LoginRequiredMixin, SuccessMessageMixin, UpdateView
):
    model = Job
    form = RegisterPaymentForm()
    fields = [*form.fields]
    success_url = reverse_lazy('jobs')
    success_message = 'Payment registered.'


class DeleteJobView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Job
    success_url = reverse_lazy('jobs')
    success_message = 'Job deleted.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteJobView, self).delete(request, *args, **kwargs)
