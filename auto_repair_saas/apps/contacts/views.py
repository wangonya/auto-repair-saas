from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView

from auto_repair_saas.apps.contacts.forms import NewContactForm
from auto_repair_saas.apps.contacts.models import Contact


class ContactsView(LoginRequiredMixin, View):
    template_name = 'contacts/index.html'
    form_class = NewContactForm

    def get(self, request):
        form = self.form_class()
        context = {
            'clients': Contact.objects.filter(contact_type='client'),
            'suppliers': Contact.objects.filter(contact_type='supplier'),
            'form': form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                Contact.objects.create(**form.cleaned_data)
                messages.success(request, 'Contact created.')
                return HttpResponseRedirect(reverse('contacts'))
            except Exception as e:
                messages.error(request, str(e))
                return HttpResponseRedirect(reverse('contacts'))
        else:
            error = 'Form is invalid.'
            messages.error(request, error)
            return HttpResponseRedirect(reverse('contacts'))


class UpdateContactView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Contact
    form = NewContactForm()
    fields = [*form.fields]
    success_url = reverse_lazy('contacts')
    success_message = 'Contact updated.'


class DeleteContactView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Contact
    success_url = reverse_lazy('contacts')
    success_message = 'Contact deleted.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteContactView, self).delete(request, *args, **kwargs)
