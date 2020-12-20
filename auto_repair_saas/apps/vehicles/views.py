from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from auto_repair_saas.apps.vehicles.forms import NewVehicleForm
from auto_repair_saas.apps.vehicles.models import Vehicle


class VehiclesView(LoginRequiredMixin, View):
    form_class = NewVehicleForm
    template_name = 'vehicles/index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                Vehicle.objects.create(**form.cleaned_data)
                vehicles = Vehicle.objects.all()
                return render(
                    request, self.template_name, {'vehicles': vehicles}
                )
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


def load_client_vehicles(request):
    owner_id = request.GET.get('client')
    try:
        vehicles = Vehicle.objects.filter(owner_id=owner_id)
    except ValueError:
        vehicles = Vehicle.objects.none()
    return render(
        request, reverse('load-vehicles'), {'vehicles': vehicles}
    )
