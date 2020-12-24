from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from auto_repair_saas.apps.contacts.models import Contact
from auto_repair_saas.apps.jobs.models import Job


class DashboardView(LoginRequiredMixin, View):
    template_name = 'dashboard/index.html'

    def get(self, request):
        context = {
            'clients': Contact.objects.filter(contact_type='client'),
            'suppliers': Contact.objects.filter(contact_type='supplier'),
            'jobs': Job.objects.all()
        }
        return render(request, self.template_name, context)
