from django.contrib.auth.views import logout_then_login
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout'),
]
