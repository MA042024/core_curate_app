""" discover rules for core main app
"""
from django.contrib.auth.models import Group, Permission
import core_main_app.permissions.rights as main_rights
import core_curate_app.permissions.rights as curate_rights


def init_rules():
    """ Init of group and permissions for the application.
    If the anonymous group does not exist, creation of the group with associate permissions
    If the default group does not exist, creation of the group with associate permissions

    Returns:

    """
    try:
        # Get or Create the default group
        default_group, created = Group.objects.get_or_create(name=main_rights.default_group)

        curate_access_perm = Permission.objects.get(codename=curate_rights.curate_access)
        curate_view_data_save_repo_perm = Permission.objects.get(codename=curate_rights.curate_view_data_save_repo)
        curate_edit_document_perm = Permission.objects.get(codename=curate_rights.curate_edit_document)
        curate_delete_document_perm = Permission.objects.get(codename=curate_rights.curate_delete_document)

        default_group.permissions.add(curate_access_perm,
                                      curate_view_data_save_repo_perm,
                                      curate_edit_document_perm,
                                      curate_delete_document_perm)
    except Exception, e:
        print('ERROR : Impossible to init the rules : ' + e.message)
