""" Test forms from `views.user.forms`.
"""
from unittest.case import TestCase
from unittest.mock import MagicMock

from django.core.exceptions import ValidationError
from django.test import override_settings

from core_curate_app.views.user.forms import (
    _file_size_validator,
    OpenForm,
    HiddenFieldsForm,
)
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


class TestHiddenFieldsForm(TestCase):
    """Test Hidden Fields Form"""

    def test_hidden_fields_form_sets_fields(self):
        """test_hidden_fields_form_sets_fields

        Returns:

        """
        form = HiddenFieldsForm(template_id="1", template_format="XSD")
        self.assertEquals(form.fields["template_id"].initial, "1")
        self.assertEquals(form.fields["template_format"].initial, "XSD")
