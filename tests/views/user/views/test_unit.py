""" Unit tests for views from `views.user.views`.
"""
from unittest.case import TestCase
from unittest.mock import patch, MagicMock

from django.http import (
    HttpResponseRedirect,
)
from django.test import RequestFactory
from django.urls import reverse

from core_curate_app.views.user.views import EnterDataView
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_parser_app.tools.parser.exceptions import ParserError


class TestEnterDataView(TestCase):
    """Test EnterDataView"""

    def setUp(self):
        """setUp
        Returns:
        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.user1.has_perm = MagicMock()
        self.user1.has_perm.return_value = True

    @patch("core_curate_app.views.user.views.EnterDataView.build_context")
    @patch("core_curate_app.views.user.views._get_curate_data_structure_by_id")
    def test_enter_data_view_get_returns_error_if_parser_error_occurs(
        self, mock_ds_get_by_id, mock_build_context
    ):
        """test_enter_data_view_get_returns_error_if_parser_error_occurs


        Returns:


        """
        # Arrange
        mock_build_context.side_effect = ParserError("error")
        mock_ds = MagicMock()
        mock_ds.form_string = "test"
        mock_ds.data = None
        mock_ds_get_by_id.return_value = mock_ds
        request = self.factory.get("core_curate_enter_data")
        request._messages = MagicMock()
        request.user = self.user1
        # Act
        response = EnterDataView.as_view()(request, curate_data_structure_id=1)
        # Assert
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertTrue(
            response.url.startswith(
                reverse("core_curate_app_xml_text_editor_view")
            )
        )
