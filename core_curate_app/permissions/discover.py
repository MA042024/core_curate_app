""" Initialize permissions for core curate app.
"""
import logging

from django.contrib.auth.models import Group, Permission

import core_curate_app.permissions.rights as curate_rights
import core_main_app.permissions.rights as main_rights

logger = logging.getLogger(__name__)


def init_permissions():
    """Initialization of groups and permissions."""
    try:
        # Get or Create the default group
        default_group, created = Group.objects.get_or_create(
            name=main_rights.default_group
        )

        # Get curate permissions
        curate_access_perm = Permission.objects.get(
            codename=curate_rights.curate_access
        )
        curate_view_data_save_repo_perm = Permission.objects.get(
            codename=curate_rights.curate_view_data_save_repo
        )

        curate_data_structure_access_perm = Permission.objects.get(
            codename=curate_rights.curate_data_structure_access
        )

        # Add permissions to default group
        default_group.permissions.add(
            curate_access_perm,
            curate_view_data_save_repo_perm,
            curate_data_structure_access_perm,
        )

    except Exception as e:
        logger.error("Impossible to init curate permissions: %s" % str(e))
