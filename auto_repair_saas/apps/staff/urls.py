from django.urls import path

from . import views

urlpatterns = [
    path('', views.StaffView.as_view(), name='staff'),
    path('search', views.StaffSearchView.as_view(), name='search-staff'),
    path('update/<int:pk>/', views.UpdateStaffView.as_view(),
         name='update-staff'),
    path('delete/<int:pk>/', views.DeleteStaffView.as_view(),
         name='delete-staff'),
]
