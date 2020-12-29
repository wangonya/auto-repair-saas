from django.urls import path

from . import views

urlpatterns = [
    path('', views.VehiclesView.as_view(), name='vehicles'),
    path('search', views.VehiclesSearchView.as_view(), name='search-vehicles'),
    path('load-vehicles', views.load_client_vehicles, name='load-vehicles'),
    path('update/<int:pk>/', views.UpdateVehicleView.as_view(),
         name='update-vehicle'),
    path('delete/<int:pk>/', views.DeleteVehicleView.as_view(),
         name='delete-vehicle'),
]
