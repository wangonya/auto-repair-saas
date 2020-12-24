from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import UpdateView, DeleteView

from auto_repair_saas.apps.vehicles.forms import NewVehicleForm
from auto_repair_saas.apps.vehicles.models import Vehicle


class VehiclesView(LoginRequiredMixin, View):
    form_class = NewVehicleForm
    template_name = 'vehicles/index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        vehicles = Vehicle.objects.all()
        context = {
            'form': form,
            'vehicles': vehicles
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                Vehicle.objects.create(**form.cleaned_data)
                messages.success(request, 'Vehicle created.')
                return HttpResponseRedirect(reverse('vehicles'))
            except Exception as e:
                messages.error(request, str(e))
                return HttpResponseRedirect(reverse('vehicles'))
        else:
            error = 'Form is invalid.'
            messages.error(request, error)
            return HttpResponseRedirect(reverse('vehicles'))


class UpdateVehicleView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Vehicle
    form = NewVehicleForm()
    fields = [*form.fields]
    success_url = reverse_lazy('vehicles')
    success_message = 'Vehicle updated.'


class DeleteVehicleView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Vehicle
    success_url = reverse_lazy('vehicles')
    success_message = 'Vehicle deleted.'

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(DeleteVehicleView, self).delete(request, *args, **kwargs)


def load_client_vehicles(request):
    owner_id = request.GET.get('client')
    try:
        vehicles = Vehicle.objects.filter(owner_id=owner_id)
    except ValueError:
        vehicles = Vehicle.objects.none()
    return render(
        request, 'vehicles/vehicle_list_options.html', {'vehicles': vehicles}
    )
