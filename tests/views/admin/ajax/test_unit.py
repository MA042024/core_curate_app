""" Unit tests for views from `views.admin.ajax`.
"""
from unittest.case import TestCase
from unittest.mock import patch

from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
)
from django.test import RequestFactory

from core_curate_app.views.admin.ajax import delete_record_drafts
from core_main_app.components.data.models import Data
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestDeleteDataDrafts(TestCase):
    """Test Delete Data Drafts"""

    def setUp(self):
        """setUp
        Returns:
        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(
            user_id="1", is_staff=True, is_superuser=True
        )

    @patch(
        "core_curate_app.components.curate_data_structure.api.delete_curate_data_structures_by_data"
    )
    @patch("core_main_app.components.data.api.get_by_id")
    def test_delete_data_drafts_returns_http_response(
        self,
        mock_data_get_by_id,
        mock_delete_data_structures,
    ):
        """test_delete_data_drafts_returns_http_response


        Returns:


        """
        mock_data_get_by_id.return_value = Data()
        mock_delete_data_structures.return_value = []
        request = self.factory.delete(
            "core-admin:core_curate_app_delete_data_drafts"
        )

        request.user = self.user1
        response = delete_record_drafts(request, 1)

        self.assertTrue(isinstance(response, HttpResponse))

    def test_delete_data_drafts_returns_error_when_data_not_found(self):
        """test_delete_data_drafts_returns_error_when_data_not_found


        Returns:


        """
        request = self.factory.delete(
            "core-admin:core_curate_app_delete_data_drafts"
        )

        request.user = self.user1
        response = delete_record_drafts(request, 1)

        self.assertTrue(isinstance(response, HttpResponseBadRequest))

    @patch(
        "core_curate_app.components.curate_data_structure.api.delete_curate_data_structures_by_data"
    )
    @patch("core_main_app.components.data.api.get_by_id")
    def test_delete_data_drafts_returns_error(
        self, mock_data_get_by_id, mock_delete_data_structures
    ):
        """test_delete_data_drafts_returns_error


        Returns:


        """
        mock_data_get_by_id.return_value = Data()
        mock_delete_data_structures.side_effect = Exception()
        request = self.factory.delete(
            "core-admin:core_curate_app_delete_data_drafts"
        )

        request.user = self.user1
        response = delete_record_drafts(request, 1)

        self.assertTrue(isinstance(response, HttpResponseBadRequest))
