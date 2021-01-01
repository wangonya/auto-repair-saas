from django.contrib.auth.views import logout_then_login
from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('logout/', logout_then_login, name='logout'),
    path('password_reset_request/', views.PasswordResetRequestView.as_view(),
         name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/',
         views.PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password_reset_done/', views.PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password_reset_complete/', views.PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
]
