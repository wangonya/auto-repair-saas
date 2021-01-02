#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import ProgrammingError


def main():
    """Run administrative tasks."""
    os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE', 'auto_repair_saas.test_settings',
    ) if 'test' in sys.argv else os.environ.setdefault(
        'DJANGO_SETTINGS_MODULE', 'auto_repair_saas.settings',
    )
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

    if 'test' not in sys.argv:
        try:
            from auto_repair_saas.apps.tenants.models import Tenant
            Tenant.objects.get(schema_name='public')
        except ObjectDoesNotExist:
            from auto_repair_saas.apps.tenants.create_tenant import \
                create_tenant
            create_tenant()
        except ProgrammingError:
            # tables not created yet
            pass


if __name__ == '__main__':
    main()
