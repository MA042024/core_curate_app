""" Curate data Structure api
"""
from core_curate_app.components.curate_data_structure.models import CurateDataStructure


def get_all():
    """ Returns all curate data structure api

    Returns:

    """
    return CurateDataStructure.get_all()


def get_by_user_id_and_template_id(user_id, template_id):
    """ Returns object with the given user id and template id

    Args:
        user_id:
        template_id:

    Returns:

    """
    return CurateDataStructure.get_by_user_id_and_template_id(user_id, template_id)
