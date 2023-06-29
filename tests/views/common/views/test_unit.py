""" Unit tests for views from `views.common.views`.
"""
from unittest.case import TestCase
from unittest.mock import patch, MagicMock

from django.test import RequestFactory

from core_curate_app.views.common.views import DraftContentEditor
from core_main_app.settings import MAX_DOCUMENT_EDITING_SIZE
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestDraftContentEditor(TestCase):
    """Test Draft Content Editor View"""

    def setUp(self):
        """setUp
        Returns:
        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")

    @patch("core_curate_app.components.curate_data_structure.api.get_by_id")
    @patch("core_main_app.utils.file.get_byte_size_from_string")
    def test_xml_content_too_big_returns_error(
        self, mock_get_byte_size, mock_ds_get_by_id
    ):
        """test_user_save_xml_content_returns_error


        Returns:


        """
        mock_ds = MagicMock()
        mock_ds.form_string = "test"
        mock_ds_get_by_id.return_value = mock_ds
        mock_get_byte_size.return_value = MAX_DOCUMENT_EDITING_SIZE + 1
        request = self.factory.get("core_main_app_xml_text_editor_view")
        request.GET = {"id": 1}
        request.user = self.user1
        response = DraftContentEditor.as_view()(request)
        self.assertTrue(
            "MAX_DOCUMENT_EDITING_SIZE" in response.content.decode()
        )
