""" Unit Test Curate Data Structure
"""
import core_curate_app.components.curate_data_structure.api as curate_data_structure_api
from core_curate_app.components.curate_data_structure.models import CurateDataStructure
from core_parser_app.components.data_structure.models import DataStructure
from core_main_app.components.template.models import Template
from unittest.case import TestCase
from mock import patch


class TestCurateDataStructureGetAll(TestCase):

    @patch.object(CurateDataStructure, 'get_all')
    def test_curate_data_get_all_return_collection_of_curate_data(self, mock_list):
        # Arrange
        mock_data_1 = CurateDataStructure(user='1', template=_get_template(), name='name_title_1')
        mock_data_2 = CurateDataStructure(user='1', template=_get_template(), name='name_title_2')
        mock_list.return_value = [mock_data_1, mock_data_2]
        # Act
        result = curate_data_structure_api.get_all()
        # Assert
        self.assertTrue(all(isinstance(item, CurateDataStructure) for item in result))


class TestCurateDataStructureGetByUserIdAndTemplateId(TestCase):

    @patch.object(DataStructure, 'get_by_user_id_and_template_id')
    def test_curate_data_structure_get_by_user_and_template_return_collection_of_curate_data_structure(self, mock_list):
        # Arrange
        mock_data_1 = CurateDataStructure(user='1', template=_get_template(), name='name_title_1')
        mock_data_2 = CurateDataStructure(user='1', template=_get_template(), name='name_title_2')
        mock_list.return_value = [mock_data_1, mock_data_2]
        # Act
        result = curate_data_structure_api.get_by_user_id_and_template_id(1, 1)
        # Assert
        self.assertTrue(all(isinstance(item, CurateDataStructure) for item in result))


def _get_template():
    template = Template()
    template.id_field = 1
    xsd = '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">' \
          '<xs:element name="tag"></xs:element></xs:schema>'
    template.content = xsd
    return template
