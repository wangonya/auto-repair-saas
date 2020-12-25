from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView

from auto_repair_saas.apps.staff.forms import NewStaffForm
from auto_repair_saas.apps.staff.models import Staff


class StaffView(LoginRequiredMixin, View):
    template_name = 'staff/index.html'
    form_class = NewStaffForm

    def get(self, request):
        form = self.form_class()
        context = {
            'staff': Staff.objects.all(),
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                Staff.objects.create(**form.cleaned_data)
                messages.success(request, 'Staff member created.')
                return HttpResponseRedirect(reverse('staff'))
            except Exception as e:
                messages.error(request, str(e))
                return HttpResponseRedirect(reverse('staff'))
        else:
            error = 'Form is invalid.'
            messages.error(request, error)
            return HttpResponseRedirect(reverse('staff'))


class UpdateStaffView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Staff
    form = NewStaffForm()
    fields = [*form.fields]
    success_url = reverse_lazy('staff')
    success_message = 'Staff member updated.'


class DeleteStaffView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Staff
    success_url = reverse_lazy('staff')
    success_message = 'Staff member deleted.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteStaffView, self).delete(request, *args, **kwargs)
