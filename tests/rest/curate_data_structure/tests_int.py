""" Integration Test for Data Structure Rest API
"""

from tests.components.curate_data_structure.fixtures.fixtures import (
    DataStructureFixtures,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_curate_app.rest.curate_data_structure import (
    views as data_structure_rest_views,
)
from rest_framework import status

from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)

fixture_data_structure = DataStructureFixtures()


class TestDataStructureListAdmin(MongoIntegrationBaseTestCase):
    fixture = fixture_data_structure

    def setUp(self):
        super(TestDataStructureListAdmin, self).setUp()

        self.user = create_mock_user("1", is_staff=True, is_superuser=True)

        self.data = {
            "user": "1",
            "name": "name",
            "form_string": "<tag></tag>",
            "template": str(self.fixture.template.id),
        }

    def test_get_returns_all_user_data_structure(self):
        # Act
        response = RequestMock.do_request_get(
            data_structure_rest_views.AdminCurateDataStructureList.as_view(), self.user
        )

        # Assert
        self.assertEqual(len(response.data), 3)

    def test_post_returns_data_structure(self):
        # Arrange

        # Act
        response = RequestMock.do_request_post(
            data_structure_rest_views.AdminCurateDataStructureList.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.data["user"], self.user.id)

        self.assertEqual(response.data["template"], str(self.fixture.template.id))

        self.assertEqual(response.data["form_string"], "<tag></tag>")

    def test_post_incorrect_parameter_returns_http_400(self):
        # Arrange
        self.data["template"] = "507f1f77bcf86cd799439011"

        # Act
        response = RequestMock.do_request_post(
            data_structure_rest_views.AdminCurateDataStructureList.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_data_structure_missing_field_returns_http_400(self):
        # Arrange
        self.data = {"user": "1", "name": "name", "form_string": "<tag></tag>"}

        # Act
        response = RequestMock.do_request_post(
            data_structure_rest_views.AdminCurateDataStructureList.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
