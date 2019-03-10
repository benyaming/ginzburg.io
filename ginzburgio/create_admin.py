#!/usr/bin/env python3
from os import environ

print(f'from django.contrib.auth.models import User; User.objects.create_superuser('
      f'"{environ.get("ADMIN_NAME")}", '
      f'"{environ.get("ADMIN_MAIL")}", '
      f'"{environ.get("ADMIN_PASS")}")'
      )
