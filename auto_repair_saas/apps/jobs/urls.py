from django.urls import path

from . import views

urlpatterns = [
    path('', views.JobsView.as_view(), name='jobs'),
    path('search', views.JobsSearchView.as_view(), name='search-jobs'),
    path('pay/<int:pk>/', views.RegisterJobPaymentView.as_view(),
         name='pay-job'),
    path('update/<int:pk>/', views.UpdateJobView.as_view(), name='update-job'),
    path('delete/<int:pk>/', views.DeleteJobView.as_view(), name='delete-job'),
]
