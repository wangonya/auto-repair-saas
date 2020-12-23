from django.urls import path

from . import views

urlpatterns = [
    path('', views.ContactsView.as_view(), name='contacts'),
    path('update/<int:pk>/', views.UpdateContactView.as_view(),
         name='update-contact'),
    path('delete/<int:pk>/', views.DeleteContactView.as_view(),
         name='delete-contact'),
]
