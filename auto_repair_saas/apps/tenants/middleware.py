import os

from django.core.exceptions import ObjectDoesNotExist
from django_tenants.middleware import TenantMainMiddleware
from django_tenants.utils import get_public_schema_name

from .create_tenant import create_tenant


class TenantMiddleware(TenantMainMiddleware):
    def get_tenant(self, domain_model, hostname, *args):
        schema_name = get_public_schema_name()
        print(f'args = {args}')
        # import pdb
        # pdb.set_trace()
        # if request.META.get('HTTP_AUTHORIZATION'):
        #     encoded_token = request.META.get('HTTP_AUTHORIZATION').split()[-1]
        #     try:
        #         decoded_token = jwt.decode(encoded_token,
        #                                    os.getenv('SECRET_KEY'),
        #                                    algorithms=['HS256'])
        #         schema_name = decoded_token.get('tenant_schema', schema_name)
        #     except PyJWTError:
        #         # invalid token
        #         pass
        try:
            domain = domain_model.objects.select_related('tenant').get(domain=schema_name)
            return domain.tenant
        except ObjectDoesNotExist:
            if schema_name == 'public':
                create_tenant()
                domain = domain_model.objects.select_related('tenant').get(domain=schema_name)
                return domain.tenant
            else:
                raise
