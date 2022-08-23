""" Integration Test for Data Structure Rest API
"""

from rest_framework import status
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from tests.components.curate_data_structure.fixtures.fixtures import (
    DataStructureFixtures,
)
from core_curate_app.rest.curate_data_structure import (
    views as data_structure_rest_views,
)


fixture_data_structure = DataStructureFixtures()


class TestDataStructureListAdmin(MongoIntegrationBaseTestCase):
    """
    Test Data Structure List Admin
    """

    fixture = fixture_data_structure

    def setUp(self):
        """setUp"""
        super().setUp()

        self.user = create_mock_user("1", is_staff=True, is_superuser=True)

        self.data = {
            "user": "1",
            "name": "name",
            "form_string": "<tag></tag>",
            "template": str(self.fixture.template.id),
        }

    def test_get_returns_all_user_data_structure(self):
        """
        test_get_returns_all_user_data_structure

        Returns:

        """
        # Act
        response = RequestMock.do_request_get(
            data_structure_rest_views.AdminCurateDataStructureList.as_view(), self.user
        )

        # Assert
        self.assertEqual(len(response.data), 3)

    def test_post_returns_data_structure(self):
        """
        test_post_returns_data_structure

        Returns:

        """

        # Act
        response = RequestMock.do_request_post(
            data_structure_rest_views.AdminCurateDataStructureList.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.data["user"], self.user.id)

        self.assertEqual(response.data["template"], self.fixture.template.id)

        self.assertEqual(response.data["form_string"], "<tag></tag>")

    def test_post_incorrect_parameter_returns_http_400(self):
        """
        test_post_incorrect_parameter_returns_http_400

        Returns:

        """
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
        """
        test_post_data_structure_missing_field_returns_http_400

        Returns:

        """
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


class TestDataStructureList(MongoIntegrationBaseTestCase):
    """
    Test Data Structure List
    """

    fixture = fixture_data_structure

    def setUp(self):
        """setUp"""
        super().setUp()

        self.superuser = create_mock_user("1", is_staff=True, is_superuser=True)

        self.user = create_mock_user("2")

        self.data = {
            "user": "2",
            "name": "name",
            "form_string": "<tag></tag>",
            "template": str(self.fixture.template.id),
        }

    def test_get_returns_all_user_data_structure_as_superuser(self):
        """
        test_get_returns_all_user_data_structure_as_superuser

        Returns:

        """
        # Act
        response = RequestMock.do_request_get(
            data_structure_rest_views.CurateDataStructureList.as_view(), self.superuser
        )

        # Assert
        self.assertEqual(len(response.data), 2)

    def test_get_returns_all_user_data_structure_as_user(self):
        """
        test_get_returns_all_user_data_structure_as_user

        Returns:

        """
        # Act
        response = RequestMock.do_request_get(
            data_structure_rest_views.CurateDataStructureList.as_view(), self.user
        )

        # Assert
        self.assertEqual(len(response.data), 1)

    def test_post_returns_http_201(self):
        """
        test_post_returns_http_201

        Returns:

        """

        # Act
        response = RequestMock.do_request_post(
            data_structure_rest_views.CurateDataStructureList.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_incorrect_parameter_returns_http_400(self):
        """
        test_post_incorrect_parameter_returns_http_400

        Returns:

        """
        # Arrange
        self.data["template"] = "507f1f77bcf86cd799439011"

        # Act
        response = RequestMock.do_request_post(
            data_structure_rest_views.CurateDataStructureList.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_data_structure_missing_field_returns_http_400(self):
        """
        test_post_data_structure_missing_field_returns_http_400

        Returns:

        """
        # Arrange
        self.data = {"user": "1", "name": "name", "form_string": "<tag></tag>"}

        # Act
        response = RequestMock.do_request_post(
            data_structure_rest_views.CurateDataStructureList.as_view(),
            self.user,
            data=self.data,
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestDataStructureDetail(MongoIntegrationBaseTestCase):
    """
    Test Data Structure Detail
    """

    fixture = fixture_data_structure

    def test_get_returns_http_200(self):
        """
        test_get_returns_http_200

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            user,
            param={"pk": str(self.fixture.data_structure_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_returns_data_structure(self):
        """
        test_get_returns_data_structure

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            user,
            param={"pk": str(self.fixture.data_structure_1.id)},
        )

        # Assert
        self.assertEqual(response.data["name"], self.fixture.data_structure_1.name)

    def test_get_other_user_data_structure_returns_http_403(self):
        """
        test_get_other_user_data_structure_returns_http_403

        Returns:

        """
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_get(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            user,
            param={"pk": str(self.fixture.data_structure_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_wrong_id_returns_http_404(self):
        """
        test_get_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_get(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_returns_http_204(self):
        """
        test_delete_returns_http_204

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_delete(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            user,
            param={"pk": str(self.fixture.data_structure_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_other_user_blob_returns_http_403(self):
        """
        test_delete_other_user_blob_returns_http_403

        Returns:

        """
        # Arrange
        user = create_mock_user("2")

        # Act
        response = RequestMock.do_request_delete(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            user,
            param={"pk": str(self.fixture.data_structure_1.id)},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_wrong_id_returns_http_404(self):
        """
        test_delete_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_delete(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_returns_updated_name(self):
        """
        test_patch_returns_updated_name

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            user,
            param={"pk": str(self.fixture.data_structure_1.id)},
            data={"name": "new_name"},
        )

        # Assert
        self.assertEqual(response.data["name"], "new_name")

    def test_patch_wrong_id_returns_http_404(self):
        """
        test_patch_wrong_id_returns_http_404

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            user,
            param={"pk": -1},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_wrong_template_returns_http_400(self):
        """
        test_patch_wrong_template_returns_http_400

        Returns:

        """
        # Arrange
        user = create_mock_user("1")

        # Act
        response = RequestMock.do_request_patch(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            user,
            data={"template": -1},
            param={"pk": self.fixture.data_structure_1.id},
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
