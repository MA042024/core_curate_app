""" Unit Test Data
"""

from mock import patch

from tests.components.curate_data_structure.fixtures.fixtures import (
    DataStructureFixtures,
)

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.integration_tests.integration_base_test_case import (
    MongoIntegrationBaseTestCase,
)

import core_curate_app.components.curate_data_structure.api as curate_data_structure_api
from core_curate_app.components.curate_data_structure.models import CurateDataStructure
from core_main_app.access_control.exceptions import AccessControlError

fixture_data_structure = DataStructureFixtures()


class TestCurateDataStructureGetById(MongoIntegrationBaseTestCase):
    fixture = fixture_data_structure

    def test_get_by_id_as_superuser_returns_data_structure(self):
        data_structure_id = self.fixture.data_structure_1.id
        mock_user = create_mock_user(
            self.fixture.data_structure_1.user, is_staff=True, is_superuser=True
        )
        data_structure = curate_data_structure_api.get_by_id(
            data_structure_id, mock_user
        )
        self.assertTrue(isinstance(data_structure, CurateDataStructure))

    def test_get_by_id_as_owner_returns_data_structure(self):
        data_structure_id = self.fixture.data_structure_1.id
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        data_structure = curate_data_structure_api.get_by_id(
            data_structure_id, mock_user
        )
        self.assertTrue(isinstance(data_structure, CurateDataStructure))

    def test_get_by_id_as_user_not_owner_raises_error(self):
        data_structure_id = self.fixture.data_structure_1.id
        mock_user = create_mock_user(self.fixture.data_structure_3.user)
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_by_id(data_structure_id, mock_user)


class TestCurateDataStructureGetAll(MongoIntegrationBaseTestCase):
    fixture = fixture_data_structure

    def test_get_all_as_superuser_returns_all_data_structure(self):
        mock_user = create_mock_user("1", is_staff=True, is_superuser=True)
        result = curate_data_structure_api.get_all(mock_user)
        self.assertTrue(all(isinstance(item, CurateDataStructure) for item in result))

    def test_get_all_as_user_raises_error(self):
        mock_user = create_mock_user("1")
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_all(mock_user)


class TestCurateDataStructureGetAllExceptUserIdWithNoData(MongoIntegrationBaseTestCase):
    fixture = fixture_data_structure

    def test_get_all_except_user_id_with_no_data_as_superuser_returns_all_data_structure_except_user(
        self,
    ):
        mock_user = create_mock_user("4", is_staff=True, is_superuser=True)
        user_id = self.fixture.data_structure_3.user
        result = curate_data_structure_api.get_all_except_user_id_with_no_data(
            user_id, mock_user
        )
        self.assertTrue(all(isinstance(item, CurateDataStructure) for item in result))
        self.assertTrue(
            all((item.user != self.fixture.data_structure_3.user) for item in result)
        )

    def test_get_all_except_user_id_with_no_data_raises_error(self):
        mock_user = create_mock_user("1")
        user_id = self.fixture.data_structure_3.user
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_all_except_user_id_with_no_data(
                user_id, mock_user
            )


class TestCurateDataStructureDelete(MongoIntegrationBaseTestCase):
    fixture = fixture_data_structure

    def test_delete_others_data_structure_as_superuser_deletes_data_structure(self):
        data_structure = self.fixture.data_structure_3
        mock_user = create_mock_user(
            self.fixture.data_structure_1.user, is_staff=True, is_superuser=True
        )
        curate_data_structure_api.delete(data_structure, mock_user)

    def test_delete_own_data_structure_deletes_data_structure(self):
        data_structure = self.fixture.data_structure_1
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        curate_data_structure_api.delete(data_structure, mock_user)

    def test_delete_others_data_structure_raises_error(self):
        data_structure = self.fixture.data_structure_3
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.delete(data_structure, mock_user)


class TestCurateDataStructureUpdateDataStructureRoot(MongoIntegrationBaseTestCase):
    fixture = fixture_data_structure

    def test_update_others_data_structure_root_as_superuser_updates_data_structure(
        self,
    ):
        data_structure = self.fixture.data_structure_1
        new_data_structure_element_root = self.fixture.data_structure_3.id
        mock_user = create_mock_user(
            self.fixture.data_structure_2.user, is_staff=True, is_superuser=True
        )
        result = curate_data_structure_api.update_data_structure_root(
            data_structure, new_data_structure_element_root, mock_user
        )
        self.assertTrue(isinstance(result, CurateDataStructure))
        self.assertTrue(
            result.data_structure_element_root, new_data_structure_element_root
        )

    def test_update_own_data_structure_root_updates_data_structure(self):
        data_structure = self.fixture.data_structure_1
        new_data_structure_element_root = self.fixture.data_structure_2.id
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        result = curate_data_structure_api.update_data_structure_root(
            data_structure, new_data_structure_element_root, mock_user
        )
        self.assertTrue(isinstance(result, CurateDataStructure))
        self.assertTrue(
            result.data_structure_element_root, new_data_structure_element_root
        )

    def test_update_others_data_structure_root_raises_error(self):
        data_structure = self.fixture.data_structure_1
        new_data_structure_element_root = self.fixture.data_structure_2.id
        mock_user = create_mock_user(self.fixture.data_structure_3.user)
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.update_data_structure_root(
                data_structure, new_data_structure_element_root, mock_user
            )


class TestCurateDataStructureCreateOrUpdate(MongoIntegrationBaseTestCase):
    fixture = fixture_data_structure

    def test_upsert_others_data_structure_as_superuser_updates_data_structure(self):
        data_structure = self.fixture.data_structure_3
        data_structure.name = "new_name_3"
        mock_user = create_mock_user(
            self.fixture.data_structure_1.user, is_staff=True, is_superuser=True
        )
        result = curate_data_structure_api.upsert(data_structure, mock_user)
        self.assertTrue(isinstance(result, CurateDataStructure))
        self.assertTrue(data_structure.name, result.name)

    def test_upsert_own_data_structure_root_updates_data_structure(self):
        data_structure = self.fixture.data_structure_1
        data_structure.name = "new_name_1"
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        result = curate_data_structure_api.upsert(data_structure, mock_user)
        self.assertTrue(isinstance(result, CurateDataStructure))
        self.assertTrue(data_structure.name, result.name)

    def test_update_others_data_structure_root_raises_error(self):
        data_structure = self.fixture.data_structure_1
        data_structure.name = "new_name_1"
        mock_user = create_mock_user(self.fixture.data_structure_3.user)
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.upsert(data_structure, mock_user)


class TestCurateDataStructureGetAllWithNoData(MongoIntegrationBaseTestCase):
    fixture = fixture_data_structure

    def test_get_all_with_no_data_as_superuser_returns_all_data_structure(
        self,
    ):
        mock_user = create_mock_user("4", is_staff=True, is_superuser=True)
        result = curate_data_structure_api.get_all_with_no_data(mock_user)
        self.assertTrue(all(isinstance(item, CurateDataStructure) for item in result))
        self.assertTrue(len(result), 3)

    def test_get_all_with_no_data_raises_error(self):
        mock_user = create_mock_user("1")
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_all_with_no_data(mock_user)


class TestCurateDataStructureGetByDataId(MongoIntegrationBaseTestCase):
    fixture = fixture_data_structure

    def test_get_by_data_id_as_superuser_returns_data_structure(self):

        mock_user = create_mock_user(
            self.fixture.data_structure_3.user, is_staff=True, is_superuser=True
        )
        data_structure = curate_data_structure_api.get_by_data_id(
            self.fixture.data.id, mock_user
        )
        self.assertTrue(isinstance(data_structure, CurateDataStructure))
        self.assertEquals(self.fixture.data.id, data_structure.data.id)

    def test_get_by_data_id_as_owner_returns_data_structure(self):
        mock_user = create_mock_user(self.fixture.data_structure_1.user)
        data_structure = curate_data_structure_api.get_by_data_id(
            self.fixture.data.id, mock_user
        )
        self.assertTrue(isinstance(data_structure, CurateDataStructure))
        self.assertEquals(self.fixture.data.id, data_structure.data.id)

    def test_get_by_data_id_as_user_not_owner_raises_error(self):
        mock_user = create_mock_user(self.fixture.data_structure_3.user)
        with self.assertRaises(AccessControlError):
            curate_data_structure_api.get_by_data_id(self.fixture.data.id, mock_user)
