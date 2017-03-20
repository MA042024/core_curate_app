from core_main_app.components.data.models import Data
from core_parser_app.components.data_structure.models import DataStructure
from django_mongoengine import fields
from mongoengine import errors as mongoengine_errors
from core_main_app.commons import exceptions


class CurateDataStructure(DataStructure):
    """ Curate data structure
    """
    form_string = fields.StringField(blank=True)
    data = fields.ReferenceField(Data, blank=True)

    @staticmethod
    def get_by_id(data_structure_id):
        """ Returns the object with the given id

        Args:
            data_structure_id:

        Returns:
            Curate Data Structure (obj): CurateDataStructure object with the given id

        """
        try:
            return CurateDataStructure.objects.get(pk=str(data_structure_id))
        except mongoengine_errors.DoesNotExist as e:
            raise exceptions.DoesNotExist(e.message)
        except Exception as ex:
            raise exceptions.ModelError(ex.message)

    @staticmethod
    def get_none():
        """ Returns None object, used by forms

        Returns:

        """
        return CurateDataStructure.objects().none()

    @staticmethod
    def get_all():
        """ Returns all curate data structure api

        Returns:

        """
        return CurateDataStructure.objects.all()

    @staticmethod
    def get_all_by_user_id_and_template_id(user_id, template_id):
        """Returns all template version managers with user set to None

        Returns:

        """
        return CurateDataStructure.objects(user=str(user_id), template=str(template_id)).all()
