from core_main_app.components.data.models import Data
from core_parser_app.components.data_structure.models import DataStructure
from django_mongoengine import fields


class CurateDataStructure(DataStructure):
    """ Curate data structure
    """
    form_string = fields.StringField(blank=True)
    data = fields.ReferenceField(Data, blank=True)

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
