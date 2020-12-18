from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from auto_repair_saas.apps.contacts.forms import NewContactForm
from auto_repair_saas.apps.contacts.models import Contact


@login_required
def contacts(request):
    context = {
        'clients': Contact.objects.filter(contact_type='client'),
        'suppliers': Contact.objects.filter(contact_type='supplier')
    }
    return render(request, 'contacts/index.html', context)


@login_required
def new_contact(request):
    if request.method == 'POST':
        form = NewContactForm(request.POST)
        if form.is_valid():
            try:
                Contact.objects.create(**form.cleaned_data)
                return HttpResponseRedirect('/contacts/')
            except Exception as e:
                error = str(e)
                return render(
                    request, 'contacts/new.html', {
                        'form': form, 'error': error
                    }
                )
        else:
            error = 'Form is invalid.'
            return render(
                request, 'contacts/new.html', {
                    'form': form, 'error': error
                }
            )
    else:
        form = NewContactForm()
    return render(request, 'contacts/new.html', {'form': form})
