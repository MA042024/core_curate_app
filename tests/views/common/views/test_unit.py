""" Unit tests for views from `views.common.views`.
"""
from unittest.case import TestCase
from unittest.mock import patch, MagicMock

from django.test import RequestFactory

from core_curate_app.views.common.views import FormView

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.labels import get_form_label


class TestFormView(TestCase):
    """Test Form View"""

    def setUp(self):
        """setUp
        Returns:
        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1", is_superuser=True)

    @patch("core_curate_app.components.curate_data_structure.api.get_by_id")
    def test_form_view_returns_error_when_xml_string_is_empty(
        self, mock_ds_get_by_id
    ):
        """test_form_view_returns_error_when_xml_string_is_empty


        Returns:


        """
        mock_ds = MagicMock()
        mock_ds.form_string = ""
        mock_ds_get_by_id.return_value = mock_ds

        request = self.factory.get("core_curate_view_form")

        request.user = self.user1
        response = FormView.as_view()(request, curate_data_structure_id=1)
        msg_error = (
            "The "
            + get_form_label()
            + " was not saved and cannot be displayed."
        )
        self.assertTrue(msg_error in response.content.decode())
