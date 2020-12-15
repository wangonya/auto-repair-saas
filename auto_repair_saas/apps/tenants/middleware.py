from django.core.exceptions import ObjectDoesNotExist
from django_tenants.middleware import TenantMainMiddleware
from django_tenants.utils import get_public_schema_name

from .create_tenant import create_tenant


class TenantMiddleware(TenantMainMiddleware):
    def get_tenant(self, domain_model, hostname, *args):
        schema_name = get_public_schema_name()
        try:
            domain = domain_model.objects.select_related('tenant').get(
                domain=schema_name
            )
            return domain.tenant
        except ObjectDoesNotExist:
            if schema_name == 'public':
                create_tenant()
                domain = domain_model.objects.select_related('tenant').get(
                    domain=schema_name
                )
                return domain.tenant
            else:
                raise
