"""Curate models
"""
from django.db import models
from core_main_app.permissions.utils import get_formatted_name
from permissions import rights


class Curate(models.Model):
    class Meta:
        verbose_name = 'core_curate_app'
        default_permissions = ()
        permissions = (
            (rights.curate_access, get_formatted_name(rights.curate_access)),
        )
