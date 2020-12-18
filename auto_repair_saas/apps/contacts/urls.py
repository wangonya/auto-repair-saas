from django.urls import path

from . import views

urlpatterns = [
    path('', views.contacts, name='contacts'),
    path('new', views.new_contact, name='new-contact'),
]
