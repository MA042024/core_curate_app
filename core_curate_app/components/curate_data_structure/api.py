""" Curate data Structure api
"""
from core_curate_app.components.curate_data_structure.models import CurateDataStructure
from core_parser_app.tools.parser import parser


def upsert(curate_data_structure):
    """ Save or update the Curate Data Structure

    Args:
        curate_data_structure:

    Returns:

    """
    return curate_data_structure.save_object()


def get_none():
    """ Returns None object, used by forms

    Returns:

    """
    return CurateDataStructure.get_none()


def get_all():
    """ Returns all curate data structure api

    Returns:

    """
    return CurateDataStructure.get_all()


def get_by_id(curate_data_structure_id):
    """ Returns the curate data structure with the given id

    Args:
        curate_data_structure_id:

    Returns:

    """
    return CurateDataStructure.get_by_id(curate_data_structure_id)


def get_all_by_user_id_and_template_id(user_id, template_id):
    """ Returns object with the given user id and template id

    Args:
        user_id:
        template_id:

    Returns:

    """
    return CurateDataStructure.get_all_by_user_id_and_template_id(user_id, template_id)


def get_by_user_id_and_template_id_and_name(user_id, template_id, name):
    """ Returns object with the given user id and template id and name

    Args:
        user_id:
        template_id:
        name:

    Returns:

    """
    return CurateDataStructure.get_by_user_id_and_template_id_and_name(user_id, template_id, name)


def delete(curate_data_structure):
    """ Deletes the curate data structure and the element associated

    Args:
        curate_data_structure:
    """

    # Delete data element structure
    if curate_data_structure.data_structure_element_root is not None:
        parser.delete_branch_from_db(curate_data_structure.data_structure_element_root.id)
    # Delete curate data structure
    curate_data_structure.delete()


def get_all_by_user_id_with_no_data(user_id):
    """ Returns all the curate date structure of the user, with no data.

    Args: user_id:
    Returns:
    """
    return CurateDataStructure.get_all_by_user_id_with_no_data(user_id)


def get_all_except_user_id_with_no_data(user_id):
    """ Returns all the curate date structure except the one of the user, with no data.

    Args: user_id:
    Returns:
    """
    return CurateDataStructure.get_all_except_user_id_with_no_data(user_id)
