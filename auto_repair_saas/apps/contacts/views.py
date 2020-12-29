from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import SearchVector
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import UpdateView, DeleteView

from auto_repair_saas.apps.contacts.forms import NewContactForm
from auto_repair_saas.apps.contacts.models import Contact
from auto_repair_saas.apps.utils.search import SearchForm


class ContactsView(LoginRequiredMixin, View):
    template_name = 'contacts/index.html'
    search_form_class = SearchForm
    contact_form_class = NewContactForm

    def get(self, request):
        contact_form = self.contact_form_class()
        search_form = self.search_form_class()
        clients = Contact.objects.filter(contact_type='client')
        suppliers = Contact.objects.filter(contact_type='supplier')
        context = {
            'clients': clients,
            'clients_count': clients.count(),
            'suppliers': suppliers,
            'suppliers_count': suppliers.count(),
            'form': contact_form,
            'search_form': search_form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.contact_form_class(request.POST)
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


class ContactsSearchView(LoginRequiredMixin, View):
    search_form_class = SearchForm
    contact_form_class = NewContactForm
    template_name = 'contacts/index.html'

    def get(self, request, *args, **kwargs):
        search_form = self.search_form_class(request.GET)
        contact_form = self.contact_form_class()

        if not search_form.is_valid():
            HttpResponseRedirect(reverse('contacts'))

        if search_form.cleaned_data.get('q') == '':
            contacts = Contact.objects.all()
        else:
            contacts = Contact.objects.annotate(
                search=SearchVector('name', 'email', 'phone'),
            ).filter(search=search_form.cleaned_data.get('q'))

        clients = contacts.filter(contact_type='client')
        suppliers = contacts.filter(contact_type='supplier')

        context = {
            'clients': clients,
            'clients_count': clients.count(),
            'suppliers': suppliers,
            'suppliers_count': suppliers.count(),
            'form': contact_form,
            'search_form': search_form
        }
        return render(
            request, self.template_name, context
        )
