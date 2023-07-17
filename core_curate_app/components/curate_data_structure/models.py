"""Curate Data Structure models
"""
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError
from django.db.models.signals import pre_delete
from core_main_app.commons import exceptions
from core_main_app.utils.validation.regex_validation import (
    not_empty_or_whitespaces,
)
from core_main_app.components.data.models import Data
from core_parser_app.components.data_structure.models import DataStructure
from core_curate_app.permissions import rights


class CurateDataStructure(DataStructure):
    """Curate data structure."""

    form_string = models.TextField(blank=True)
    data = models.ForeignKey(
        Data, blank=True, on_delete=models.CASCADE, null=True
    )

    @staticmethod
    def get_permission():
        """get_permission

        Returns:

        """
        return f"{rights.CURATE_CONTENT_TYPE}.{rights.CURATE_DATA_STRUCTURE_ACCESS}"

    def save_object(self):
        """Custom save

        Returns:

        """
        try:
            self.clean()
            return self.save()
        except IntegrityError:
            raise exceptions.NotUniqueError(
                "Unable to save the document: not unique."
            )
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_by_id(data_structure_id):
        """Return the object with the given id.

        Args:
            data_structure_id:

        Returns:
            Curate Data Structure (obj): CurateDataStructure object with the given id

        """
        try:
            return CurateDataStructure.objects.get(pk=str(data_structure_id))
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_none():
        """Return None object, used by forms.

        Returns:

        """
        return CurateDataStructure.objects.none()

    @staticmethod
    def get_all():
        """Return all curate data structure api.

        Returns:

        """
        return CurateDataStructure.objects.all()

    @staticmethod
    def get_all_by_user_id_and_template_id(user_id, template_id):
        """Return all template version managers with user set to None.

        Returns:

        """
        return CurateDataStructure.objects.filter(
            user=str(user_id), template=str(template_id)
        ).all()

    @staticmethod
    def get_by_user_id_and_template_id_and_name(user_id, template_id, name):
        """Return the curate data structure with user, template id and name.

        Returns:

        """
        try:
            return CurateDataStructure.objects.get(
                user=str(user_id), template=str(template_id), name=name
            )
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_all_by_user_id_with_no_data(user_id):
        """
        Return all the curate date structure of the user, with no data.

        Args: user_id:
        Return:
        """
        return CurateDataStructure.objects.filter(
            user=str(user_id), data__isnull=True
        ).all()

    @staticmethod
    def get_all_except_user_id_with_no_data(user_id):
        """Return all the curate date structure except the one of the user, with no data.

        Args: user_id:
        Return:
        """
        return (
            CurateDataStructure.objects.exclude(user=str(user_id))
            .filter(data__isnull=True)
            .all()
        )

    @staticmethod
    def get_all_by_user_id_and_template_id_with_no_data(user_id, template_id):
        """

        Args:
            user_id:
            template_id:

        Returns:

        """
        return CurateDataStructure.objects.filter(
            user=str(user_id), template=str(template_id), data__isnull=True
        ).all()

    @staticmethod
    def get_all_with_no_data():
        """Returns all curate data structure api with no link to a data.

        Args:

        Returns:

        """
        return CurateDataStructure.objects.filter(data__isnull=True).all()

    @staticmethod
    def get_all_by_user(user_id):
        """Return all curate data structure by user.

        Returns:

        """
        return CurateDataStructure.objects.filter(user=str(user_id)).all()

    @staticmethod
    def get_by_data_id_and_user(data_id, user_id):
        """Return the curate data structure with the given data id and user

        Args:
            data_id:
            user_id:

        Returns:

        """
        try:
            return CurateDataStructure.objects.get(
                data=str(data_id), user=str(user_id)
            )
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    @staticmethod
    def get_by_data_structure_element_root(data_structure_element_root):
        """Return the curate data structure with the given data id

        Args:
            data_structure_element_root:

        Returns:

        """
        try:
            return CurateDataStructure.objects.get(
                data_structure_element_root=str(data_structure_element_root.id)
            )
        except ObjectDoesNotExist as exception:
            raise exceptions.DoesNotExist(str(exception))
        except Exception as exception:
            raise exceptions.ModelError(str(exception))

    def clean(self):
        """Clean before saving

        Returns:

        """
        not_empty_or_whitespaces(self.name)
        self.name = self.name.strip()

    @staticmethod
    def get_all_curate_data_structures_by_data(data):
        """Get All Curate Data Structures By Data.

        Args:
            data:

        Returns:

        """

        return CurateDataStructure.objects.filter(data=data.id).all()


# Connect signals
pre_delete.connect(DataStructure.pre_delete, sender=CurateDataStructure)
