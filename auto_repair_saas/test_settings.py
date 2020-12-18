from .settings import *

INSTALLED_APPS.remove('django_tenants')
INSTALLED_APPS.remove('auto_repair_saas.apps.tenants')
MIDDLEWARE.remove('auto_repair_saas.apps.tenants.middleware.TenantMiddleware')
