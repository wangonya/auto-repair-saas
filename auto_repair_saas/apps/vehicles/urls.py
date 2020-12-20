from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', views.VehiclesView.as_view(), name='vehicles'),
    path('load-vehicles', views.load_client_vehicles, name='load-vehicles'),
]
