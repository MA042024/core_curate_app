""" ACL Test Data Structure
"""
from django.contrib.auth.models import AnonymousUser
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_parser_app.components.data_structure.models import (
    DataStructureElement,
)
from core_curate_app.components.curate_data_structure.models import (
    CurateDataStructure,
)
import core_curate_app.components.curate_data_structure.api as curate_data_structure_api

from tests.components.curate_data_structure.fixtures.fixtures import (
    DataStructureFixtures,
)


fixture_data_structure = DataStructureFixtures()


class TestCurateDataStructureGetById(IntegrationBaseTestCase):
    """
    Test Curate Data Structure Get ById
    """

    fixture = fixture_data_structure

    def test_get_by_id_as_superuser_returns_data_structure(self):
        """
        test_get_by_id_as_superuser_returns_data_structure

        Returns:

        """
        data_structure_id = self.fixture.data_structure_1.id
        mock_user = create_mock_user(
            self.fixture.data_structure_1.user,
            is_staff=True,
            is_superuser=True,
        )
        data_structure = curate_data_structure_api.get_by_id(
            data_structure_id, mock_user
        )
        self.assertTrue(isinstance(data_structure, CurateDataStructure))

    def test_get_by_id_as_owner_returns_data_structure(self):
        """
        test_get_by_id_as_owner_returns_data_structure

        Returns:

        """
        data_structure_id = self.fixture.data_structure_1.id
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        data_structure = curate_data_structure_api.get_by_id(
            data_structure_id, mock_user
        )
        self.assertTrue(isinstance(data_structure, CurateDataStructure))

    def test_get_by_id_as_user_non_owner_raises_error(self):
        """
        test_get_by_id_as_user_non_owner_raises_error

        Returns:

        """
        data_structure_id = self.fixture.data_structure_1.id
        mock_user = create_mock_user(self.fixture.data_structure_3.user)
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_by_id(data_structure_id, mock_user)

    def test_get_by_id_as_anonymous_user_raises_error(self):
        """
        test_get_by_id_as_anonymous_user_raises_error

        Returns:

        """
        data_structure_id = self.fixture.data_structure_1.id
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_by_id(
                data_structure_id, AnonymousUser()
            )


class TestCurateDataStructureGetAll(IntegrationBaseTestCase):
    """
    Test Curate Data Structure Get All
    """

    fixture = fixture_data_structure

    def test_get_all_as_superuser_returns_all_data_structure(self):
        """
        test_get_all_as_superuser_returns_all_data_structure

        Returns:

        """
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)
        result = curate_data_structure_api.get_all(mock_user)
        self.assertTrue(
            all(isinstance(item, CurateDataStructure) for item in result)
        )

    def test_get_all_as_user_raises_error(self):
        """
        test_get_all_as_user_raises_error

        Returns:

        """
        mock_user = create_mock_user("1")
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_all(mock_user)

    def test_get_all_as_anonymous_user_raises_error(self):
        """
        test_get_all_as_anonymous_user_raises_error

        Returns:

        """
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_all(AnonymousUser())


class TestCurateDataStructureGetAllExceptUserIdWithNoData(
    IntegrationBaseTestCase
):
    """
    Test Curate Data Structure Get All Except User Id With No Data
    """

    fixture = fixture_data_structure

    def test_get_all_except_user_id_with_no_data_as_superuser_returns_all_data_structure_except_user(
        self,
    ):
        """
        test_get_all_except_user_id_with_no_data_as_superuser_returns_all_data_structure_except_user

        Returns:

        """
        mock_user = create_mock_user("4", is_staff=True, is_superuser=True)
        user_id = self.fixture.data_structure_3.user
        result = curate_data_structure_api.get_all_except_user_id_with_no_data(
            user_id, mock_user
        )
        self.assertTrue(
            all(isinstance(item, CurateDataStructure) for item in result)
        )
        self.assertTrue(
            all(
                (item.user != self.fixture.data_structure_3.user)
                for item in result
            )
        )
        self.assertTrue(all((item.data is None) for item in result))

    def test_get_all_except_user_id_with_no_data_as_user_raises_error(self):
        """
        test_get_all_except_user_id_with_no_data_as_user_raises_error

        Returns:

        """
        mock_user = create_mock_user("1")
        user_id = self.fixture.data_structure_3.user
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_all_except_user_id_with_no_data(
                user_id, mock_user
            )

    def test_get_all_except_user_id_with_no_data_as_anonymous_user_raises_error(
        self,
    ):
        """
        test_get_all_except_user_id_with_no_data_as_anonymous_user_raises_error

        Returns:

        """
        user_id = self.fixture.data_structure_3.user
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_all_except_user_id_with_no_data(
                user_id, AnonymousUser()
            )


class TestCurateDataStructureDelete(IntegrationBaseTestCase):
    """
    Test Curate Data Structure Delete
    """

    fixture = fixture_data_structure

    def test_delete_others_data_structure_as_superuser_deletes_data_structure(
        self,
    ):
        """
        test_delete_others_data_structure_as_superuser_deletes_data_structure

        Returns:

        """
        data_structure = self.fixture.data_structure_3
        mock_user = create_mock_user(
            self.fixture.data_structure_1.user,
            is_staff=True,
            is_superuser=True,
        )
        curate_data_structure_api.delete(data_structure, mock_user)

    def test_delete_own_data_structure_deletes_data_structure(self):
        """
        test_delete_own_data_structure_deletes_data_structure

        Returns:

        """
        data_structure = self.fixture.data_structure_1
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        curate_data_structure_api.delete(data_structure, mock_user)

    def test_delete_others_data_structure_as_user_raises_error(self):
        """
        test_delete_others_data_structure_as_user_raises_error

        Returns:

        """
        data_structure = self.fixture.data_structure_3
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.delete(data_structure, mock_user)

    def test_delete_others_data_structure_as_anonymous_user_raises_error(self):
        """
        test_delete_others_data_structure_as_anonymous_user_raises_error

        Returns:

        """
        data_structure = self.fixture.data_structure_3
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.delete(data_structure, AnonymousUser())


class TestCurateDataStructureUpdateDataStructureRoot(IntegrationBaseTestCase):
    """
    Test Curate Data Structure Update Data Structure Root
    """

    fixture = fixture_data_structure

    def test_update_others_data_structure_root_as_superuser_updates_data_structure(
        self,
    ):
        """
        test_update_others_data_structure_root_as_superuser_updates_data_structure

        Returns:

        """
        data_structure = self.fixture.data_structure_1
        new_data_structure_element_root = _get_data_structure_element(
            self.fixture.data_structure_3.user, self.fixture.data_structure_3
        )
        mock_user = create_mock_user(
            self.fixture.data_structure_2.user,
            is_staff=True,
            is_superuser=True,
        )
        result = curate_data_structure_api.update_data_structure_root(
            data_structure, new_data_structure_element_root, mock_user
        )
        self.assertTrue(isinstance(result, CurateDataStructure))
        self.assertTrue(
            result.data_structure_element_root, new_data_structure_element_root
        )

    def test_update_own_data_structure_root_updates_data_structure(self):
        """
        test_update_own_data_structure_root_updates_data_structure

        Returns:

        """
        data_structure = self.fixture.data_structure_1
        new_data_structure_element_root = _get_data_structure_element(
            self.fixture.data_structure_2.user, self.fixture.data_structure_2
        )
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        result = curate_data_structure_api.update_data_structure_root(
            data_structure, new_data_structure_element_root, mock_user
        )
        self.assertTrue(isinstance(result, CurateDataStructure))
        self.assertTrue(
            result.data_structure_element_root, new_data_structure_element_root
        )

    def test_update_others_data_structure_root_as_user_raises_error(self):
        """
        test_update_others_data_structure_root_as_user_raises_error

        Returns:

        """
        data_structure = self.fixture.data_structure_1
        new_data_structure_element_root = self.fixture.data_structure_2.id
        mock_user = create_mock_user(self.fixture.data_structure_3.user)
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.update_data_structure_root(
                data_structure, new_data_structure_element_root, mock_user
            )

    def test_update_others_data_structure_root_as_anonymous_user_raises_error(
        self,
    ):
        """
        test_update_others_data_structure_root_as_anonymous_user_raises_error

        Returns:

        """
        data_structure = self.fixture.data_structure_1
        new_data_structure_element_root = self.fixture.data_structure_2.id
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.update_data_structure_root(
                data_structure,
                new_data_structure_element_root,
                AnonymousUser(),
            )


class TestCurateDataStructureCreateOrUpdate(IntegrationBaseTestCase):
    """
    Test Curate Data Structure Create Or Update
    """

    fixture = fixture_data_structure

    def test_upsert_others_data_structure_as_superuser_updates_data_structure(
        self,
    ):
        """
        test_upsert_others_data_structure_as_superuser_updates_data_structure

        Returns:

        """
        data_structure = self.fixture.data_structure_3
        data_structure.name = "new_name_3"
        mock_user = create_mock_user(
            self.fixture.data_structure_1.user,
            is_staff=True,
            is_superuser=True,
        )
        result = curate_data_structure_api.upsert(data_structure, mock_user)
        self.assertTrue(isinstance(result, CurateDataStructure))
        self.assertTrue(data_structure.name, result.name)

    def test_upsert_own_data_structure_updates_data_structure(self):
        """
        test_upsert_own_data_structure_updates_data_structure

        Returns:

        """
        data_structure = self.fixture.data_structure_1
        data_structure.name = "new_name_1"
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        result = curate_data_structure_api.upsert(data_structure, mock_user)
        self.assertTrue(isinstance(result, CurateDataStructure))
        self.assertTrue(data_structure.name, result.name)

    def test_upsert_others_data_structure_as_user_raises_error(self):
        """
        test_upsert_others_data_structure_as_user_raises_error

        Returns:

        """
        data_structure = self.fixture.data_structure_1
        data_structure.name = "new_name_1"
        mock_user = create_mock_user(self.fixture.data_structure_3.user)
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.upsert(data_structure, mock_user)

    def test_upsert_data_structure_as_anonymous_user_raises_error(self):
        """
        test_upsert_data_structure_as_anonymous_user_raises_error

        Returns:

        """
        data_structure = self.fixture.data_structure_1
        data_structure.name = "new_name_1"
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.upsert(data_structure, AnonymousUser())


class TestCurateDataStructureGetAllWithNoData(IntegrationBaseTestCase):
    """
    Test Curate Data Structure Get All With No Data
    """

    fixture = fixture_data_structure

    def test_get_all_with_no_data_as_superuser_returns_all_data_structure(
        self,
    ):
        """
        test_get_all_with_no_data_as_superuser_returns_all_data_structure

        Returns:

        """
        mock_user = create_mock_user("4", is_staff=True, is_superuser=True)
        result = curate_data_structure_api.get_all_with_no_data(mock_user)
        self.assertTrue(
            all(isinstance(item, CurateDataStructure) for item in result)
        )
        self.assertTrue(len(result), 3)

    def test_get_all_with_no_data_as_user_raises_error(self):
        """
        test_get_all_with_no_data_as_user_raises_error

        Returns:

        """
        mock_user = create_mock_user("1")
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_all_with_no_data(mock_user)

    def test_get_all_with_no_data_as_anonymous_user_raises_error(self):
        """
        test_get_all_with_no_data_as_anonymous_user_raises_error

        Returns:

        """
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_all_with_no_data(AnonymousUser())


class TestCurateDataStructureGetByDataId(IntegrationBaseTestCase):
    """
    Test Curate Data Structure Get ById
    """

    fixture = fixture_data_structure

    def test_get_by_data_id_as_owner_returns_data_structure(self):
        """
        test_get_by_data_id_as_owner_returns_data_structure

        Returns:

        """
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        data_structure = curate_data_structure_api.get_by_data_id_and_user(
            self.fixture.data.id, mock_user
        )
        self.assertTrue(isinstance(data_structure, CurateDataStructure))
        self.assertEquals(self.fixture.data.id, data_structure.data.id)

    def test_get_by_data_id_as_anonymous_user_raises_error(self):
        """
        test_get_by_data_id_as_anonymous_user_raises_error

        Returns:

        """
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_by_data_id_and_user(
                self.fixture.data.id, AnonymousUser()
            )


class TestDataStructureChangeOwner(IntegrationBaseTestCase):
    """
    Test Data Structure Change Owner
    """

    fixture = fixture_data_structure

    def test_change_owner_from_owner_to_owner_ok(self):
        """
        test_change_owner_from_owner_to_owner_ok

        Returns:

        """
        mock_owner = create_mock_user(self.fixture.data_structure_1.user)
        curate_data_structure_api.change_owner(
            document=fixture_data_structure.data_structure_1,
            new_user=mock_owner,
            user=mock_owner,
        )

    def test_change_owner_from_owner_to_user_ok(self):
        """
        test_change_owner_from_owner_to_user_ok

        Returns:

        """
        mock_owner = create_mock_user(self.fixture.data_structure_1.user)
        mock_user = create_mock_user("2")
        curate_data_structure_api.change_owner(
            document=fixture_data_structure.data_structure_1,
            new_user=mock_user,
            user=mock_owner,
        )

    def test_change_owner_from_user_to_user_raises_exception(self):
        """
        test_change_owner_from_user_to_user_raises_exception

        Returns:

        """
        mock_owner = create_mock_user("0")
        mock_user = create_mock_user("2")
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.change_owner(
                document=fixture_data_structure.data_structure_1,
                new_user=mock_user,
                user=mock_owner,
            )

    def test_change_owner_from_anonymous_to_user_raises_exception(self):
        """
        test_change_owner_from_anonymous_to_user_raises_exception

        Returns:

        """

        mock_user = create_mock_user("2")
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.change_owner(
                document=fixture_data_structure.data_structure_1,
                new_user=mock_user,
                user=AnonymousUser(),
            )

    def test_change_owner_as_superuser_ok(self):
        """
        test_change_owner_as_superuser_ok

        Returns:

        """
        mock_user = create_mock_user("2", is_superuser=True)
        curate_data_structure_api.change_owner(
            document=fixture_data_structure.data_structure_1,
            new_user=mock_user,
            user=mock_user,
        )


class TestGetAllCurateDataStructureByData(IntegrationBaseTestCase):
    """
    Test Get All Curate Data Structures By Data
    """

    fixture = fixture_data_structure

    def test_get_all_curate_data_structures_by_data_as_superuser_returns_data_structures(
        self,
    ):
        """
        test_get_all_curate_data_structures_by_data_as_superuser_returns_data_structures

        Returns:

        """

        mock_user = create_mock_user(
            self.fixture.data_structure_3.user,
            is_staff=True,
            is_superuser=True,
        )
        results = (
            curate_data_structure_api.get_all_curate_data_structures_by_data(
                self.fixture.data, mock_user
            )
        )
        for data_structure in results:
            self.assertTrue(isinstance(data_structure, CurateDataStructure))

    def test_get_all_curate_data_structures_by_data_as_user_raises_error(
        self,
    ):
        """
        test_get_all_curate_data_structures_by_data_as_user_raises_error

        Returns:

        """
        mock_user = create_mock_user(self.fixture.data_structure_3.user)
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_all_curate_data_structures_by_data(
                self.fixture.data, mock_user
            )

    def test_get_all_curate_data_structures_by_data_as_anonymous_user_raises_error(
        self,
    ):
        """
        test_get_all_curate_data_structures_by_data_as_anonymous_user_raises_error

        Returns:

        """
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_all_curate_data_structures_by_data(
                self.fixture.data, AnonymousUser()
            )


def _get_data_structure_element(user, data_structure):
    """Return a data structure element

    Args:
        user:
        data_structure:

    Returns:

    """
    data_structure_element = DataStructureElement(
        user=user,
        tag="tag",
        value="value",
        options={},
        data_structure=data_structure,
    )
    data_structure_element.save()
    return data_structure_element
