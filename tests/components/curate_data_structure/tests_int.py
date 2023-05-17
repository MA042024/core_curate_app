""" ACL Test Data Structure
"""
from django.contrib.auth.models import AnonymousUser

from core_main_app.access_control.exceptions import AccessControlError

from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user

from core_curate_app.components.curate_data_structure.models import (
    CurateDataStructure,
)
import core_curate_app.components.curate_data_structure.api as curate_data_structure_api

from tests.components.curate_data_structure.fixtures.fixtures import (
    DataStructureFixtures2,
)


fixture_data_structure = DataStructureFixtures2()


class TestGetCurateDataStructuresByData(IntegrationBaseTestCase):
    """
    Test Get Curate Data Structures By Data
    """

    fixture = fixture_data_structure

    def test_get_all_curate_data_structures_by_data_returns_data_structure_list(
        self,
    ):
        """
        test_get_all_curate_data_structures_by_data_returns_data_structure_list

        Returns:

        """
        mock_user = create_mock_user(
            self.fixture.data_structure_1.user, is_superuser=True
        )
        result = (
            curate_data_structure_api.get_all_curate_data_structures_by_data(
                self.fixture.data, mock_user
            )
        )
        for data_structure in result:
            self.assertTrue(isinstance(data_structure, CurateDataStructure))

    def test_get_all_curate_data_structures_by_data_returns_empty_list_when_data_has_no_data_structure(
        self,
    ):
        """
        test_get_all_curate_data_structures_by_data_returns_empty_list_when_data_has_no_data_structure

        Returns:

        """
        mock_user = create_mock_user("0", is_superuser=True)
        result = (
            curate_data_structure_api.get_all_curate_data_structures_by_data(
                self.fixture.data_without_draft, mock_user
            )
        )
        self.assertEqual(list(result), [])

    def test_get_all_curate_data_structures_by_data_as_user_raise_error(
        self,
    ):
        """
        test_get_all_curate_data_structures_by_data_as_user_raise_error

        Returns:

        """
        mock_user = create_mock_user("1")

        # Act # Assert
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_all_curate_data_structures_by_data(
                self.fixture.data_multiple_drafts, mock_user
            )

    def test_get_all_curate_data_structures_by_data_as_anonymous_raise_error(
        self,
    ):
        """
        test_get_all_curate_data_structures_by_data_as_anonymous_raise_error

        Returns:

        """

        # Act # Assert
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_all_curate_data_structures_by_data(
                self.fixture.data_multiple_drafts, AnonymousUser()
            )


class TestDeleteCurateDataStructuresByData(IntegrationBaseTestCase):
    """
    Test Delete Curate Data Structures By Data
    """

    fixture = fixture_data_structure

    def test_delete_curate_data_structures_by_data_deletes_curate_data_structures(
        self,
    ):
        """
        test_delete_curate_data_structures_by_data_deletes_curate_data_structures

        Returns:

        """
        mock_user = create_mock_user("1", is_superuser=True, is_staff=True)
        curate_data_structure_api.delete_curate_data_structures_by_data(
            self.fixture.data, mock_user
        )

    def test_delete_curate_data_structures_by_data_returns_none(
        self,
    ):
        """
        test_delete_curate_data_structures_by_data_returns_none

        Returns:

        """
        mock_user = create_mock_user("0", is_superuser=True)
        curate_data_structure_api.delete_curate_data_structures_by_data(
            self.fixture.data_without_draft, mock_user
        )

    def test_delete_curate_data_structures_by_data_raise_error(
        self,
    ):
        """
        test_delete_curate_data_structures_by_data_raise_error

        Returns:

        """
        mock_user = create_mock_user("1")

        # Act # Assert
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.delete_curate_data_structures_by_data(
                self.fixture.data_multiple_drafts, mock_user
            )

    def test_delete_curate_data_structures_by_data_raise_error_as_anonymous_raise_error(
        self,
    ):
        """
        test_delete_curate_data_structures_by_data_raise_error_as_anonymous_raise_error

        Returns:

        """

        # Act # Assert
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.delete_curate_data_structures_by_data(
                self.fixture.data_multiple_drafts, AnonymousUser()
            )
