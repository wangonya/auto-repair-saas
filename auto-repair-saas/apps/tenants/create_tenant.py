#!/usr/bin/env python

from datetime import date

# from celery import shared_task
from dateutil.relativedelta import relativedelta
from django.db import DatabaseError
from django.db.utils import IntegrityError

from .models import Tenant, Domain


# @shared_task
def create_tenant(schema_name='public',
                  name='public',
                  paid_until=None,
                  on_trial=True):
    try:
        if not paid_until:
            # set paid until date one month from now for trial period
            paid_until = date.today() + relativedelta(months=+1)
        tenant = Tenant(schema_name=schema_name,
                        name=name,
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
            # public schema already exists - this will most likely happen when running migrations
            pass
        else:
            raise DatabaseError(f'An error occurred while setting up the tenant schema: {e}')
    except Exception as e:
        raise DatabaseError(
            f'An error occurred while setting up the tenant schema: {e}')
