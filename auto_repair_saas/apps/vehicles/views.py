from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from auto_repair_saas.apps.vehicles.forms import NewVehicleForm


class VehiclesView(View):
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
                return HttpResponseRedirect('/vehicles/')
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
