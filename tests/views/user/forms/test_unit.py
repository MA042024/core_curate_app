""" Test forms from `views.user.forms`.
"""
from unittest.case import TestCase
from unittest.mock import MagicMock

from django.test import override_settings
from django.core.exceptions import ValidationError

from core_curate_app.views.user.forms import _file_size_validator, OpenForm
from core_main_app.settings import MAX_DOCUMENT_EDITING_SIZE


class TestFileSizeValidator(TestCase):
    """Test _file_size_validator"""

    def test_file_size_validator_raises_error_when_file_too_large(
        self,
    ):
        """test_file_size_validator_raises_error_when_file_too_large

        Returns:

        """
        mock_field = MagicMock()
        mock_field.size = MAX_DOCUMENT_EDITING_SIZE + 1
        with self.assertRaises(ValidationError):
            _file_size_validator(mock_field)

    def test_file_size_validator_raises_ok_when_file_size_under_limit(
        self,
    ):
        """test_file_size_validator_raises_ok_when_file_size_under_limit

        Returns:

        """
        mock_field = MagicMock()
        mock_field.size = MAX_DOCUMENT_EDITING_SIZE - 1
        _file_size_validator(mock_field)


class TestOpenForm(TestCase):
    """Test Open Form"""

    @override_settings(BOOTSTRAP_VERSION="4.6.2")
    def test_open_form_bootstrap_v4(self):
        """test_open_form_bootstrap_v4

        Returns:

        """
        data = {"forms": "test"}
        form = OpenForm(data)
        self.assertEquals(
            form.fields["forms"].widget.attrs["class"], "form-control"
        )

    @override_settings(BOOTSTRAP_VERSION="5.1.3")
    def test_open_form_bootstrap_v5(self):
        """test_open_form_bootstrap_v5

        Returns:

        """
        data = {"forms": "test"}
        form = OpenForm(data)
        self.assertEquals(
            form.fields["forms"].widget.attrs["class"], "form-select"
        )
