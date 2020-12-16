from django.db import connection
from django_tenants.middleware import TenantMainMiddleware
from django_tenants.utils import get_tenant_domain_model


class TenantMiddleware(TenantMainMiddleware):
    def process_request(self, request):
        # Connection needs first to be at the public schema, as this is where
        # the tenant metadata is stored.
        connection.set_schema_to_public()

        if request.user.is_authenticated:
            hostname = request.user.schema
        else:
            hostname = 'public'

        domain_model = get_tenant_domain_model()
        try:
            tenant = self.get_tenant(domain_model, hostname)
        except domain_model.DoesNotExist:
            raise self.TENANT_NOT_FOUND_EXCEPTION(
                'No tenant for hostname "%s"' % hostname)

        tenant.domain_url = hostname
        request.tenant = tenant

        connection.set_tenant(request.tenant)
