from django.urls import path

from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/data', views.DashboardDataView.as_view(),
         name='dashboard-data'),
]
