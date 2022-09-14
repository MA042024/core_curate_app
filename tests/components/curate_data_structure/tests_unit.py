""" Unit Test Curate Data Structure
"""
from unittest.case import TestCase

from mock import patch

from core_main_app.commons import exceptions
from core_main_app.components.template.models import Template
from core_main_app.utils.tests_tools.MockUser import create_mock_user
import core_curate_app.components.curate_data_structure.api as curate_data_structure_api
from core_curate_app.components.curate_data_structure.models import CurateDataStructure


class TestCurateDataStructureGetById(TestCase):
    """
    Test Curate Data Structure Get By Id
    """

    @patch.object(CurateDataStructure, "get_by_id")
    def test_curate_data_structure_get_by_id_raises_does_not_exist_error_if_not_found(
        self, mock_get
    ):
        """
        test_curate_data_structure_get_by_id_raises_does_not_exist_error_if_not_found

        Returns:

        """
        # Arrange
        mock_get.side_effect = exceptions.DoesNotExist("")
        mock_user = create_mock_user("1")

        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            curate_data_structure_api.get_by_id(1, mock_user)

    def test_data_structure_get_by_id_raises_does_not_exist_error_if_not_found(self):
        """
        test_data_structure_get_by_id_raises_does_not_exist_error_if_not_found

        Returns:

        """
        # Arrange
        mock_user = create_mock_user("1")

        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            curate_data_structure_api.get_by_id(1, mock_user)

    @patch.object(CurateDataStructure, "get_by_id")
    def test_curate_data_structure_get_by_id_return_data_if_found(self, mock_get):
        """
        test_curate_data_structure_get_by_id_return_data_if_found

        Returns:

        """
        # Arrange
        mock_data_structure = CurateDataStructure(
            user="1", template=Template(), name="name"
        )
        mock_get.return_value = mock_data_structure
        mock_user = create_mock_user("1")
        # Act
        result = curate_data_structure_api.get_by_id(1, mock_user)
        # Assert
        self.assertIsInstance(result, CurateDataStructure)


class TestCurateDataStructureUpsert(TestCase):
    """
    Test Curate Data Structure Upsert
    """

    @patch.object(CurateDataStructure, "save_object")
    def test_curate_data_structure_upsert_return_data_structure_element(
        self, mock_save
    ):
        """
        test_curate_data_structure_upsert_return_data_structure_element

        Returns:

        """
        # Arrange
        mock_data_structure = CurateDataStructure(
            user="1", template=Template(), name="name"
        )
        mock_save.return_value = mock_data_structure
        mock_user = create_mock_user("1")
        # Act
        result = curate_data_structure_api.upsert(mock_data_structure, mock_user)
        # Assert
        self.assertIsInstance(result, CurateDataStructure)


class TestCurateDataStructureGetAll(TestCase):
    """
    Test Curate Data Structure Get All
    """

    @patch.object(CurateDataStructure, "get_all")
    def test_curate_data_get_all_return_collection_of_curate_data(self, mock_list):
        """
        test_curate_data_get_all_return_collection_of_curate_data

        Returns:

        """
        # Arrange
        mock_data_1 = CurateDataStructure(
            user="1", template=_get_template(), name="name_title_1"
        )
        mock_data_2 = CurateDataStructure(
            user="1", template=_get_template(), name="name_title_2"
        )
        mock_list.return_value = [mock_data_1, mock_data_2]
        # Act
        result = curate_data_structure_api.get_all(
            create_mock_user("1", is_staff=True, is_superuser=True)
        )
        # Assert
        self.assertTrue(all(isinstance(item, CurateDataStructure) for item in result))


class TestCurateDataStructureGetByUserIdAndTemplateId(TestCase):
    """
    Test Curate Data Structure Get By User Id And Template Id
    """

    @patch.object(CurateDataStructure, "get_all_by_user_id_and_template_id")
    def test_curate_data_structure_get_all_by_user_and_template_return_collection(
        self, mock_list
    ):
        """
        test_curate_data_structure_get_all_by_user_and_template_return_collection

        Returns:

        """
        # Arrange
        mock_data_1 = CurateDataStructure(
            user="1", template=_get_template(), name="name_title_1"
        )
        mock_data_2 = CurateDataStructure(
            user="1", template=_get_template(), name="name_title_2"
        )
        mock_list.return_value = [mock_data_1, mock_data_2]

        # Act
        result = curate_data_structure_api.get_all_by_user_id_and_template_id(1, 1)
        # Assert
        self.assertTrue(all(isinstance(item, CurateDataStructure) for item in result))


class TestCurateDataStructureGetByUserIdAndTemplateIdAndName(TestCase):
    """
    Test Curate Data Structure Get By User Id And Template Id And Name
    """

    @patch.object(CurateDataStructure, "get_by_user_id_and_template_id_and_name")
    def test_curate_data_structure_get_by_user_and_template_and_name_return_curate_data_structure(
        self, mock_get
    ):
        """
        test_curate_data_structure_get_by_user_and_template_and_name_return_curate_data_structure

        Returns:

        """
        # Arrange
        mock_data_1 = CurateDataStructure(
            user="1", template=_get_template(), name="name_title_1"
        )
        mock_get.return_value = mock_data_1
        # Act
        result = curate_data_structure_api.get_by_user_id_and_template_id_and_name(
            1, 1, "name_title_1"
        )
        # Assert
        self.assertIsInstance(result, CurateDataStructure)

    @patch.object(CurateDataStructure, "get_by_user_id_and_template_id_and_name")
    def test_curate_data_structure_get_by_user_and_template_and_name_raises_error_if_not_found(
        self, mock_get
    ):
        """
        test_curate_data_structure_get_by_user_and_template_and_name_raises_error_if_not_found

        Returns:

        """
        # Arrange
        mock_get.side_effect = exceptions.DoesNotExist("")
        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            curate_data_structure_api.get_by_user_id_and_template_id_and_name(
                1, 1, "name_title_1"
            )

    def test_data_structure_get_by_user_and_template_and_name_raises_error_if_not_found(
        self,
    ):
        """
        test_data_structure_get_by_user_and_template_and_name_raises_error_if_not_found

        Returns:

        """

        # Act # Assert
        with self.assertRaises(exceptions.DoesNotExist):
            curate_data_structure_api.get_by_user_id_and_template_id_and_name(
                1, 1, "name_title_1"
            )


class TestCurateDataStructureGetAllByUserIdWithNoData(TestCase):
    """
    Test Curate Data Structure Get All By User Id With No Data
    """

    @patch.object(CurateDataStructure, "get_all_by_user_id_with_no_data")
    def test_curate_data_structure_get_all_by_user_id_with_no_data_return_curate_data_structure(
        self, mock_list
    ):
        """
        test_curate_data_structure_get_all_by_user_id_with_no_data_return_curate_data_structure

        Returns:

        """
        # Arrange
        mock_data_1 = CurateDataStructure(
            user="1", template=_get_template(), name="name_title_1"
        )
        mock_data_2 = CurateDataStructure(
            user="1", template=_get_template(), name="name_title_2"
        )
        mock_list.return_value = [mock_data_1, mock_data_2]
        # Act
        result = curate_data_structure_api.get_all_by_user_id_with_no_data(1)
        # Assert
        self.assertTrue(all(isinstance(item, CurateDataStructure) for item in result))


class TestCurateDataStructureGetAllExceptUserIdWithNoData(TestCase):
    """
    Test Curate Data Structure Get All Except User Id With No Data
    """

    @patch.object(CurateDataStructure, "get_all_except_user_id_with_no_data")
    def test_curate_data_structure_get_all_except_user_id_with_no_data_return_curate_data_structure(
        self, mock_list
    ):
        """
        test_curate_data_structure_get_all_except_user_id_with_no_data_return_curate_data_structure

        Returns:

        """
        # Arrange
        mock_data_1 = CurateDataStructure(
            user="1", template=_get_template(), name="name_title_1"
        )
        mock_data_2 = CurateDataStructure(
            user="1", template=_get_template(), name="name_title_2"
        )
        mock_list.return_value = [mock_data_1, mock_data_2]
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        # Act
        result = curate_data_structure_api.get_all_except_user_id_with_no_data(
            2, mock_user
        )
        # Assert
        self.assertTrue(all(isinstance(item, CurateDataStructure) for item in result))


class TestCurateDataStructureGetAllByUserIdAndTemplateIdWithNoData(TestCase):
    """
    Test Curate Data Structure Get All By User Id And Template Id With No Data
    """

    @patch.object(
        CurateDataStructure, "get_all_by_user_id_and_template_id_with_no_data"
    )
    def test_curate_data_structure_get_all_by_user_id_and_template_id_with_no_data_returns_data(
        self, mock_list
    ):
        """
        test_curate_data_structure_get_all_by_user_id_and_template_id_with_no_data_returns_data

        Returns:

        """

        # Arrange
        template = _get_template()
        mock_data_1 = CurateDataStructure(
            user="1", template=template, name="name_title_1"
        )
        mock_data_2 = CurateDataStructure(
            user="1", template=template, name="name_title_2"
        )
        mock_list.return_value = [mock_data_1, mock_data_2]
        # Act
        result = (
            curate_data_structure_api.get_all_by_user_id_and_template_id_with_no_data(
                "1", template.id
            )
        )
        # Assert
        self.assertTrue(all(isinstance(item, CurateDataStructure) for item in result))


class TestCurateDataStructureGetByUserId(TestCase):
    """
    Test Curate Data Structure Get By User Id
    """

    @patch.object(CurateDataStructure, "get_all_by_user")
    def test_curate_data_structure_get_all_by_user_return_collection_of_curate_data_structure(
        self, mock_list
    ):
        """
        test_curate_data_structure_get_all_by_user_return_collection_of_curate_data_structure

        Returns:

        """
        # Arrange
        mock_data_1 = CurateDataStructure(
            user="1", template=_get_template(), name="name_title_1"
        )
        mock_data_2 = CurateDataStructure(
            user="1", template=_get_template(), name="name_title_2"
        )
        mock_list.return_value = [mock_data_1, mock_data_2]
        # Act
        result = curate_data_structure_api.get_all_by_user(create_mock_user(1))
        # Assert
        self.assertTrue(all(isinstance(item, CurateDataStructure) for item in result))


def _get_template():
    template = Template()
    template.id_field = 1
    xsd = (
        '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
        '<xs:element name="tag"></xs:element></xs:schema>'
    )
    template.content = xsd
    return template
