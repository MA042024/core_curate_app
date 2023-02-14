""" Test forms
"""
from unittest.case import TestCase
from unittest.mock import MagicMock

from django.core.exceptions import ValidationError

from core_curate_app.views.user.forms import _file_size_validator
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
