"""Curate models
"""

from django.db import models

from core_curate_app.permissions import rights
from core_main_app.permissions.utils import get_formatted_name


class Curate(models.Model):
    class Meta(object):
        verbose_name = "core_curate_app"
        default_permissions = ()
        permissions = (
            (rights.curate_access, get_formatted_name(rights.curate_access)),
            (
                rights.curate_view_data_save_repo,
                get_formatted_name(rights.curate_view_data_save_repo),
            ),
            (
                rights.curate_data_structure_access,
                get_formatted_name(rights.curate_data_structure_access),
            ),
        )
