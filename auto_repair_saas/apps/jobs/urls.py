from django.urls import path

from . import views

urlpatterns = [
    path('', views.JobsView.as_view(), name='jobs'),
    path('new', views.NewJobView.as_view(), name='new-job'),
]
