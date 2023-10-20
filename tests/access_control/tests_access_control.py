""" Unit Test Access Control
"""
from unittest.case import TestCase

from core_curate_app.components.curate_data_structure.models import (
    CurateDataStructure,
)
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.components.template.models import Template
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_curate_app.access_control import api as access_control_api


class TestAccessControlCheckCanWrite(TestCase):
    """Test Access Control Check Can Write"""

    def setUp(self):
        """setUp"""
        self.anonymous_user = create_mock_user(user_id=None, is_anonymous=True)
        self.user1 = create_mock_user(user_id="1")
        self.superuser = create_mock_user(user_id="1", is_superuser=True)

    def test_access_control_check_can_write_as_none_raises_access_control_error(
        self,
    ):
        """test_access_control_check_can_write_as_none_raises_access_control_error

        Returns:

        """
        # Arrange
        data_structure = CurateDataStructure(
            user="1",
            template=Template(),
            name="name",
        )

        # Act # Assert
        with self.assertRaises(AccessControlError):
            access_control_api.check_can_write(data_structure, user=None)

    def test_access_control_check_can_write_as_anonymous_raises_access_control_error(
        self,
    ):
        """test_access_control_check_can_write_as_anonymous_raises_access_control_error

        Returns:

        """
        # Arrange
        data_structure = CurateDataStructure(
            user="1",
            template=Template(),
            name="name",
        )

        # Act # Assert
        with self.assertRaises(AccessControlError):
            access_control_api.check_can_write(
                data_structure, user=self.anonymous_user
            )

    def test_access_control_check_can_write_as_user_raises_access_control_error(
        self,
    ):
        """test_access_control_check_can_write_as_user_raises_access_control_error

        Returns:

        """
        # Arrange
        data_structure = CurateDataStructure(
            user="2",
            template=Template(),
            name="name",
        )

        # Act # Assert
        with self.assertRaises(AccessControlError):
            access_control_api.check_can_write(data_structure, user=self.user1)

    def test_access_control_check_can_write_as_superuser_returns_none(
        self,
    ):
        """test_access_control_check_can_write_as_superuser_returns_none

        Returns:

        """
        # Arrange
        data_structure = CurateDataStructure(
            user="2",
            template=Template(),
            name="name",
        )

        # Act # Assert
        access_control_api.check_can_write(data_structure, user=self.superuser)

    def test_access_control_check_can_write_as_owner_returns_none(
        self,
    ):
        """test_access_control_check_can_write_as_owner_returns_none

        Returns:

        """
        # Arrange
        data_structure = CurateDataStructure(
            user="1",
            template=Template(),
            name="name",
        )

        # Act # Assert
        access_control_api.check_can_write(data_structure, user=self.superuser)
