""" Curate data Structure api
"""
from core_main_app.access_control.api import has_perm_administration
from core_main_app.access_control.decorators import access_control
from core_curate_app.access_control.api import can_read, can_write, can_change_owner
from core_curate_app.components.curate_data_structure.models import CurateDataStructure


@access_control(can_write)
def upsert(curate_data_structure, user):
    """Save or update the Curate Data Structure

    Args:
        curate_data_structure:
        user:

    Returns:

    """
    curate_data_structure.save_object()
    return curate_data_structure


def get_none():
    """Returns None object, used by forms

    Returns:

    """
    return CurateDataStructure.get_none()


@access_control(has_perm_administration)
def get_all(user):
    """Returns all curate data structure api

    Returns:

    """
    return CurateDataStructure.get_all()


@access_control(can_read)
def get_by_id(curate_data_structure_id, user):
    """Returns the curate data structure with the given id

    Args:
        curate_data_structure_id:
        user:

    Returns:

    """
    return CurateDataStructure.get_by_id(curate_data_structure_id)


def get_all_by_user_id_and_template_id(user_id, template_id):
    """Returns object with the given user id and template id

    Args:
        user_id:
        template_id:

    Returns:

    """
    return CurateDataStructure.get_all_by_user_id_and_template_id(user_id, template_id)


def get_by_user_id_and_template_id_and_name(user_id, template_id, name):
    """Returns object with the given user id and template id and name

    Args:
        user_id:
        template_id:
        name:

    Returns:

    """
    return CurateDataStructure.get_by_user_id_and_template_id_and_name(
        user_id, template_id, name
    )


@access_control(can_write)
def delete(curate_data_structure, user):
    """Deletes the curate data structure and the element associated

    Args:
        curate_data_structure:
        user:
    """
    curate_data_structure.delete()


def get_all_by_user_id_with_no_data(user_id):
    """Returns all the curate date structure of the user, with no data.

    Args:
        user_id:
    Returns:
    """
    return CurateDataStructure.get_all_by_user_id_with_no_data(user_id)


@access_control(has_perm_administration)
def get_all_except_user_id_with_no_data(user_id, user):
    """Returns all the curate date structure except the one of the user, with no data.

    Args:
        user_id:
    Returns:
    """
    return CurateDataStructure.get_all_except_user_id_with_no_data(user_id)


def get_all_by_user_id_and_template_id_with_no_data(user_id, template_id):
    """Return all the curate data structure by user and template, with no link to a data

    Args:
        user_id:
        template_id:

    Returns:

    """
    return CurateDataStructure.get_all_by_user_id_and_template_id_with_no_data(
        user_id, template_id
    )


@access_control(has_perm_administration)
def get_all_with_no_data(user):
    """Returns all curate data structure api with no link to a data.

    Returns:

    """
    return CurateDataStructure.get_all_with_no_data()


@access_control(can_read)
def get_by_data_id(data_id, user):
    """Return the curate data structure with the given data id

    Args:
        data_id:

    Returns:

    """
    return CurateDataStructure.get_by_data_id(data_id)


@access_control(can_read)
def get_all_by_user(user):
    """Get all curate data that belong to user.

    Args:
        user: User

    Returns:

    """
    return CurateDataStructure.get_all_by_user(user.id)


@access_control(can_write)
def update_data_structure_root(curate_data_structure, root_element, user):
    """Update the data structure with a root element.

    Args:
        curate_data_structure:
        root_element:

    Returns:

    """
    # Delete data structure elements
    curate_data_structure.delete_data_structure_elements_from_root()

    # set the root element in the data structure
    curate_data_structure.data_structure_element_root = root_element

    # save the data structure
    upsert(curate_data_structure, user)

    return curate_data_structure


@access_control(can_read)
def get_by_data_structure_element_root_id(data_structure_element_root, user):
    """Return the curate data structure with the given data structure element root id

    Args:
        data_structure_element_root:
        user:

    Returns:

    """
    return CurateDataStructure.get_by_data_structure_element_root(
        data_structure_element_root
    )


@access_control(can_change_owner)
def change_owner(curate_data_structure, new_user, user):
    """Change curate data structure's owner.

    Args:
        curate_data_structure:
        user:
        new_user:

    Returns:
    """
    curate_data_structure.user = str(new_user.id)
    curate_data_structure.save_object()
