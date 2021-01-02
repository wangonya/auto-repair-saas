#!/usr/bin/env python

from django.db import DatabaseError
from django.db.utils import IntegrityError

from .models import Tenant, Domain


def create_tenant(schema_name='public',
                  paid_until=None,
                  on_trial=False):
    try:
        tenant = Tenant(schema_name=schema_name,
                        paid_until=paid_until,
                        on_trial=on_trial)
        tenant.save()
        domain = Domain()
        domain.domain = tenant.schema_name
        domain.tenant = tenant
        domain.is_primary = True
        domain.save()
    except IntegrityError as e:
        if '(domain_url)=(public) already exists.' in e.args[0]:
            # public schema already exists
            # this will most likely happen when running migrations
            pass
        else:
            raise DatabaseError(
                f'An error occurred while setting up the tenant schema: {e}'
            )
    except Exception as e:
        raise DatabaseError(
            f'An error occurred while setting up the tenant schema: {e}'
        )
