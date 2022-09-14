"""Curate models
"""

from django.db import models

from core_main_app.permissions.utils import get_formatted_name
from core_curate_app.permissions import rights


class Curate(models.Model):
    """Curate"""

    class Meta:
        """Meta"""

        verbose_name = "core_curate_app"
        default_permissions = ()
        permissions = (
            (rights.CURATE_ACCESS, get_formatted_name(rights.CURATE_ACCESS)),
            (
                rights.CURATE_VIEW_DATA_SAVE_REPO,
                get_formatted_name(rights.CURATE_VIEW_DATA_SAVE_REPO),
            ),
            (
                rights.CURATE_DATA_STRUCTURE_ACCESS,
                get_formatted_name(rights.CURATE_DATA_STRUCTURE_ACCESS),
            ),
        )
