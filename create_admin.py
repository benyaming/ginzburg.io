#!/usr/bin/env python3
from os import environ
from django.contrib.auth.models import User

User.objects.create_superuser(environ.get('ADMIN_NAME'), environ.get('ADMIN_MAIL'), environ.get('ADMIN_PASS'))
