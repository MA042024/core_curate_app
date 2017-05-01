""" discover rules for core main app
"""
from django.contrib.auth.models import Group, Permission
import core_main_app.permissions.rights as main_rights
import core_curate_app.permissions.rights as curate_rights


def init_permissions():
    """ Initialization of groups and permissions

    Returns:

    """
    try:
        # Get or Create the default group
        default_group, created = Group.objects.get_or_create(name=main_rights.default_group)

        # Get curate permissions
        curate_access_perm = Permission.objects.get(codename=curate_rights.curate_access)

        # Add permissions to default group
        default_group.permissions.add(curate_access_perm)

    except Exception, e:
        print('ERROR : Impossible to init the permissions : ' + e.message)
