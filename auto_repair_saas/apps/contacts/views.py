from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from auto_repair_saas.apps.contacts.forms import NewContactForm
from auto_repair_saas.apps.contacts.models import Contact


class ContactsView(LoginRequiredMixin, View):
    template_name = 'contacts/index.html'

    def get(self, request):
        context = {
            'clients': Contact.objects.filter(contact_type='client'),
            'suppliers': Contact.objects.filter(contact_type='supplier')
        }
        return render(request, self.template_name, context)


class NewContactView(LoginRequiredMixin, View):
    form_class = NewContactForm
    template_name = 'contacts/new.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                Contact.objects.create(**form.cleaned_data)
                return HttpResponseRedirect(reverse('contacts'))
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
