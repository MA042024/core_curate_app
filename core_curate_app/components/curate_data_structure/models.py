""" Curate data structure
"""
from core_parser_app.components.data_structure.models import DataStructure


class CurateDataStructure(DataStructure):
    """Data structure of Curate app"""
    # TODO: add id of existing data from core main app ?

    @staticmethod
    def get_all():
        """ Returns all curate data structure api

        Returns:

        """
        return CurateDataStructure.objects.all()

    @staticmethod
    def get_by_user_id_and_template_id(user_id, template_id):
        """Returns all template version managers with user set to None

        Returns:

        """
        return super(CurateDataStructure, CurateDataStructure).get_by_user_id_and_template_id(user_id, template_id)
