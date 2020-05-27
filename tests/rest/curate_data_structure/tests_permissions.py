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

    @patch.object(CurateDataStructureSerializer, "data")
    @patch.object(CurateDataStructureSerializer, "save")
    @patch.object(CurateDataStructureSerializer, "is_valid")
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
