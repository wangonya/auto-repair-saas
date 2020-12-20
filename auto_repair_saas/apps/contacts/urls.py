from django.urls import path

from . import views

urlpatterns = [
    path('', views.ContactsView.as_view(), name='contacts'),
    path('new', views.NewContactView.as_view(), name='new-contact'),
]
