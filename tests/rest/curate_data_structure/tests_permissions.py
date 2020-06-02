""" Authentication tests for Data Structure REST API
"""
from django.test import SimpleTestCase
from mock.mock import patch
from rest_framework import status

from core_curate_app.rest.curate_data_structure import (
    views as data_structure_rest_views,
)
from core_curate_app.components.curate_data_structure.models import CurateDataStructure
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock
from core_curate_app.rest.curate_data_structure.serializers import (
    CurateDataStructureSerializer,
)
from core_curate_app.rest.curate_data_structure.admin_serializers import (
    CurateDataStructureAdminSerializer,
)
import core_curate_app.components.curate_data_structure.api as data_structure_api


class TestDataStructureListAdminPostPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_post(
            data_structure_rest_views.AdminCurateDataStructureList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_post(
            data_structure_rest_views.AdminCurateDataStructureList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_returns_http_403(self):
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_post(
            data_structure_rest_views.AdminCurateDataStructureList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(CurateDataStructureAdminSerializer, "data")
    @patch.object(CurateDataStructureAdminSerializer, "save")
    @patch.object(CurateDataStructureAdminSerializer, "is_valid")
    def test_superuser_returns_http_201(
        self,
        data_structure_serializer_data,
        data_structure_serializer_save,
        data_structure_serializer_valid,
    ):
        data_structure_serializer_valid.return_value = True
        data_structure_serializer_save.return_value = None
        data_structure_serializer_data.return_value = {}

        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_post(
            data_structure_rest_views.AdminCurateDataStructureList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class TestDataStructureListAdminGetPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(
            data_structure_rest_views.AdminCurateDataStructureList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_returns_http_403(self):
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            data_structure_rest_views.AdminCurateDataStructureList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_returns_http_403(self):
        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_get(
            data_structure_rest_views.AdminCurateDataStructureList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(CurateDataStructure, "get_all")
    def test_superuser_returns_http_200(self, get_all):

        get_all.return_value = {}
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_get(
            data_structure_rest_views.AdminCurateDataStructureList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataStructureListGetPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(
            data_structure_rest_views.CurateDataStructureList.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(CurateDataStructure, "get_all")
    def test_authenticated_returns_http_200(self, get_all):
        get_all.return_value = {}
        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            data_structure_rest_views.CurateDataStructureList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(CurateDataStructure, "get_all")
    def test_superuser_returns_http_200(self, get_all):
        get_all.return_value = {}
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)

        response = RequestMock.do_request_get(
            data_structure_rest_views.CurateDataStructureList.as_view(), mock_user
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataStructureDetailGetPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_get(
            data_structure_rest_views.CurateDataStructureDetail.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(CurateDataStructureSerializer, "data")
    @patch.object(data_structure_api, "get_by_id")
    def test_authenticated_returns_http_200(
        self, mock_data_structure_api_get_by_id, mock_data_structure_serializer
    ):
        mock_data_structure_api_get_by_id.return_value = []
        mock_data_structure_serializer.return_value = []

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_get(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            mock_user,
            param={"pk": "0"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(CurateDataStructureSerializer, "data")
    @patch.object(data_structure_api, "get_by_id")
    def test_staff_returns_http_200(
        self, mock_data_structure_api_get_by_id, mock_data_structure_serializer
    ):
        mock_data_structure_api_get_by_id.return_value = []
        mock_data_structure_serializer.return_value = []

        mock_user = create_mock_user(
            "1",
            is_staff=True,
        )

        response = RequestMock.do_request_get(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            mock_user,
            param={"pk": "0"},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class TestDataStructureDetailDeletePermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_delete(
            data_structure_rest_views.CurateDataStructureDetail.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(data_structure_api, "delete")
    @patch.object(data_structure_api, "get_by_id")
    def test_authenticated_returns_http_204(
        self, mock_data_structure_api_get_by_id, mock_data_structure_api_delete
    ):
        mock_data_structure_api_get_by_id.return_value = None
        mock_data_structure_api_delete.return_value = None

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_delete(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch.object(data_structure_api, "delete")
    @patch.object(data_structure_api, "get_by_id")
    def test_staff_returns_http_204(
        self, mock_data_structure_api_get_by_id, mock_data_structure_api_delete
    ):
        mock_data_structure_api_get_by_id.return_value = None
        mock_data_structure_api_delete.return_value = None

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_delete(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class TestDataStructureDetailPatchPermissions(SimpleTestCase):
    def test_anonymous_returns_http_403(self):
        response = RequestMock.do_request_patch(
            data_structure_rest_views.CurateDataStructureDetail.as_view(), None
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @patch.object(CurateDataStructureSerializer, "data")
    @patch.object(CurateDataStructureSerializer, "save")
    @patch.object(CurateDataStructureSerializer, "is_valid")
    @patch.object(data_structure_api, "get_by_id")
    def test_authenticated_returns_http_200(
        self,
        mock_data_structure_api_get_by_id,
        mock_data_structure_serializer,
        mock_data_structure_serializer_save,
        mock_data_structure_serializer_is_valid,
    ):
        mock_data_structure_api_get_by_id.return_value = []
        mock_data_structure_serializer_is_valid.return_value = True
        mock_data_structure_serializer_save.return_value = None
        mock_data_structure_serializer.return_value = []

        mock_user = create_mock_user("1")

        response = RequestMock.do_request_patch(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch.object(CurateDataStructureSerializer, "data")
    @patch.object(CurateDataStructureSerializer, "save")
    @patch.object(CurateDataStructureSerializer, "is_valid")
    @patch.object(data_structure_api, "get_by_id")
    def test_staff_returns_http_200(
        self,
        mock_data_structure_api_get_by_id,
        mock_data_structure_serializer_is_valid,
        mock_data_structure_serializer_save,
        mock_data_structure_serializer,
    ):
        mock_data_structure_api_get_by_id.return_value = []
        mock_data_structure_serializer_is_valid.return_value = True
        mock_data_structure_serializer_save.return_value = None
        mock_data_structure_serializer.return_value = []

        mock_user = create_mock_user("1", is_staff=True)

        response = RequestMock.do_request_patch(
            data_structure_rest_views.CurateDataStructureDetail.as_view(),
            mock_user,
            param={"pk": 0},
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
