""" Initialize permissions for core curate app.
"""
import logging

from django.contrib.auth.models import Group, Permission
import core_main_app.permissions.rights as main_rights
import core_curate_app.permissions.rights as curate_rights


logger = logging.getLogger(__name__)


def init_permissions():
    """Initialization of groups and permissions."""
    try:
        # Get or Create the default group
        default_group, created = Group.objects.get_or_create(
            name=main_rights.DEFAULT_GROUP
        )

        # Get curate permissions
        curate_access_perm = Permission.objects.get(
            codename=curate_rights.CURATE_ACCESS
        )
        curate_view_data_save_repo_perm = Permission.objects.get(
            codename=curate_rights.CURATE_VIEW_DATA_SAVE_REPO
        )

        curate_data_structure_access_perm = Permission.objects.get(
            codename=curate_rights.CURATE_DATA_STRUCTURE_ACCESS
        )

        # Add permissions to default group
        default_group.permissions.add(
            curate_access_perm,
            curate_view_data_save_repo_perm,
            curate_data_structure_access_perm,
        )

    except Exception as exception:
        logger.error("Impossible to init curate permissions: %s", str(exception))
