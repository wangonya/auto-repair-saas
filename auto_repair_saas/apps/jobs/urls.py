from django.urls import path

from . import views

urlpatterns = [
    path('', views.JobsView.as_view(), name='jobs'),
    path('update/<int:pk>/', views.UpdateJobView.as_view(), name='update-job'),
    path('delete/<int:pk>/', views.DeleteJobView.as_view(), name='delete-job'),
]
