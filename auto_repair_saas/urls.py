"""auto URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from auto_repair_saas.apps.tenants.views import seed_data

urlpatterns = [
    path('', include('auto_repair_saas.apps.dashboard.urls')),
    path('jobs/', include('auto_repair_saas.apps.jobs.urls')),
    path('vehicles/', include('auto_repair_saas.apps.vehicles.urls')),
    path('contacts/', include('auto_repair_saas.apps.contacts.urls')),
    path('auth/', include('auto_repair_saas.apps.authentication.urls')),
    path('seed/', seed_data, name='seed-data'),
    path('admin/', admin.site.urls),
]
