from django.urls import path

from . import views

urlpatterns = [
    path('', views.jobs, name='jobs'),
    path('new', views.new_job, name='new-job'),
]
