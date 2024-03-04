""" Test access to views from `views.common.views`.
"""
import json
from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory

from core_curate_app.views.common.views import (
    DataStructureXMLEditor,
    DataStructureJSONEditor,
)
from core_main_app.settings import MAX_DOCUMENT_EDITING_SIZE
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests.components.curate_data_structure.fixtures.fixtures import (
    DataStructureFixtures,
)

fixture_data_structure = DataStructureFixtures()


class TestDataStructureXMLEditorView(IntegrationBaseTestCase):
    """Test Draft Content Editor View"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.anonymous = AnonymousUser()
        self.fixture = DataStructureFixtures()
        self.fixture.insert_data()

    def test_get_assets(self):
        """test_get_assets

        Returns:

        """
        instance = DataStructureXMLEditor()
        DataStructureXMLEditor._get_assets(instance)

    def test_anonymous_user_can_not_access_to_draft(self):
        """test_anonymous_user_can_not_access_to_draft

        Returns:

        """
        request = self.factory.get("core_curate_app_xml_text_editor_view")
        request.user = self.anonymous
        request.GET = {"id": str(self.fixture.data_structure_1.id)}
        response = DataStructureXMLEditor.as_view()(request)
        self.assertTrue(
            self.fixture.data_structure_1.name not in response.content.decode()
        )
        self.assertTrue("Error 403" in response.content.decode())

    def test_user_can_not_access_to_draft_if_not_found(self):
        """test_user_can_not_access_to_draft_if_not_found

        Returns:

        """
        request = self.factory.get("core_curate_app_xml_text_editor_view")
        request.GET = {"id": "-1"}
        request.user = self.user1
        response = DataStructureXMLEditor.as_view()(request)
        self.assertTrue("Error 404" in response.content.decode())

    def test_user_can_not_access_to_draft_if_missing_param(self):
        """test_user_can_not_access_to_draft_if_missing_param

        Returns:

        """
        request = self.factory.get("core_curate_app_xml_text_editor_view")
        request.user = self.user1
        response = DataStructureXMLEditor.as_view()(
            request,
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_access_to_draft_if_owner(self):
        """test_user_can_access_a_draft_if_owner

        Returns:

        """
        request = self.factory.get("core_curate_app_xml_text_editor_view")
        request.GET = {"id": str(self.fixture.data_structure_1.id)}
        request.user = self.user1
        response = DataStructureXMLEditor.as_view()(
            request,
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_access_to_data_draft_if_owner(self):
        """test_user_can_access_to_data_draft_if_owner

        Returns:

        """
        request = self.factory.get("core_curate_app_xml_text_editor_view")
        request.GET = {"data_id": str(self.fixture.data.id)}
        request.user = self.user1
        response = DataStructureXMLEditor.as_view()(
            request,
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_save_xml_content(self):
        """test_user_can_save_xml_content

        Returns:

        """
        data = {
            "content": "<tag></tag>",
            "action": "save",
            "document_id": str(self.fixture.data_structure_2.id),
            "id": str(self.fixture.data_structure_2.id),
        }
        request = self.factory.post(
            "core_curate_app_xml_text_editor_view", data
        )
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user1
        response = DataStructureXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_can_save_data_draft_xml_content(self):
        """test_user_can_save_data_draft_xml_content

        Returns:

        """
        data = {
            "content": "<tag></tag>",
            "action": "save",
            "document_id": str(self.fixture.data_structure_1.id),
            "id": str(self.fixture.data_structure_1.id),
        }
        request = self.factory.post(
            "core_curate_app_xml_text_editor_view", data
        )
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user1
        response = DataStructureXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_save_xml_content_returns_acl_error(self):
        """test_user_save_xml_content_returns_acl_error

        Returns:

        """
        data = {
            "content": "<tag></tag>",
            "action": "save",
            "document_id": str(self.fixture.data_structure_1.id),
            "id": str(self.fixture.data_structure_1.id),
        }
        request = self.factory.post(
            "core_curate_app_xml_text_editor_view", data
        )
        request.user = self.anonymous
        response = DataStructureXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_user_save_xml_content_returns_dne_error(self):
        """test_user_save_xml_content_returns_dne_error

        Returns:

        """
        data = {
            "content": "<tag></tag>",
            "action": "save",
            "document_id": "-1",
            "id": "-1",
        }
        request = self.factory.post(
            "core_curate_app_xml_text_editor_view", data
        )
        request.user = self.user1
        response = DataStructureXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_save_xml_content_returns_error(self):
        """test_user_save_xml_content_returns_error

        Returns:

        """
        data = {
            "action": "save",
            "document_id": "-1",
            "id": "-1",
        }
        request = self.factory.post(
            "core_curate_app_xml_text_editor_view", data
        )
        request.user = self.user1
        response = DataStructureXMLEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    @patch("core_main_app.utils.file.get_byte_size_from_string")
    def test_json_content_too_big_returns_error(self, mock_get_byte_size):
        """test_json_content_too_big_returns_error

        Returns:

        """
        mock_get_byte_size.return_value = MAX_DOCUMENT_EDITING_SIZE + 1
        request = self.factory.get("core_curate_app_json_text_editor_view")
        request.GET = {"id": str(self.fixture.data_structure_1.id)}
        request.user = self.user1
        response = DataStructureXMLEditor.as_view()(request)
        self.assertTrue(
            "MAX_DOCUMENT_EDITING_SIZE" in response.content.decode()
        )


class TestDataStructureJSONEditorView(IntegrationBaseTestCase):
    """Test Draft Content Editor View"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="3")
        self.anonymous = AnonymousUser()
        self.fixture = DataStructureFixtures()
        self.fixture.insert_data()

    def test_get_assets(self):
        """test_get_assets

        Returns:

        """
        instance = DataStructureJSONEditor()
        DataStructureJSONEditor._get_assets(instance)

    def test_anonymous_user_can_not_access_to_draft(self):
        """test_anonymous_user_can_not_access_to_draft

        Returns:

        """
        request = self.factory.get("core_curate_app_json_text_editor_view")
        request.user = self.anonymous
        request.GET = {"id": str(self.fixture.data_structure_json_1.id)}
        response = DataStructureJSONEditor.as_view()(request)
        self.assertTrue(
            self.fixture.data_structure_json_1.name
            not in response.content.decode()
        )
        self.assertTrue("Error 403" in response.content.decode())

    def test_user_can_not_access_to_draft_if_not_found(self):
        """test_user_can_not_access_to_draft_if_not_found

        Returns:

        """
        request = self.factory.get("core_curate_app_json_text_editor_view")
        request.GET = {"id": "-1"}
        request.user = self.user1
        response = DataStructureJSONEditor.as_view()(request)
        self.assertTrue("Error 404" in response.content.decode())

    def test_user_can_not_access_to_draft_if_missing_param(self):
        """test_user_can_not_access_to_draft_if_missing_param

        Returns:

        """
        request = self.factory.get("core_curate_app_json_text_editor_view")
        request.user = self.user1
        response = DataStructureJSONEditor.as_view()(
            request,
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_access_to_draft_if_owner(self):
        """test_user_can_access_a_draft_if_owner

        Returns:

        """
        request = self.factory.get("core_curate_app_json_text_editor_view")
        request.GET = {"id": str(self.fixture.data_structure_json_1.id)}
        request.user = self.user1
        response = DataStructureJSONEditor.as_view()(
            request,
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_access_to_data_draft_if_owner(self):
        """test_user_can_access_to_data_draft_if_owner

        Returns:

        """
        request = self.factory.get("core_curate_app_json_text_editor_view")
        request.GET = {"data_id": str(self.fixture.data_json.id)}
        request.user = self.user1
        response = DataStructureJSONEditor.as_view()(
            request,
        )
        self.assertEqual(response.status_code, 200)

    def test_user_can_save_json_content(self):
        """test_user_can_save_json_content

        Returns:

        """
        data = {
            "content": "{}",
            "action": "save",
            "document_id": str(self.fixture.data_structure_json_2.id),
            "id": str(self.fixture.data_structure_json_2.id),
        }
        request = self.factory.post(
            "core_curate_app_json_text_editor_view", data
        )
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user1
        response = DataStructureJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_can_save_data_draft_json_content(self):
        """test_user_can_save_data_draft_json_content

        Returns:

        """
        data = {
            "content": "{}",
            "action": "save",
            "document_id": str(self.fixture.data_structure_json_1.id),
            "id": str(self.fixture.data_structure_json_1.id),
        }
        request = self.factory.post(
            "core_curate_app_json_text_editor_view", data
        )
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user1
        response = DataStructureJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_user_save_json_content_returns_acl_error(self):
        """test_user_save_json_content_returns_acl_error

        Returns:

        """
        data = {
            "content": "{}",
            "action": "save",
            "document_id": str(self.fixture.data_structure_json_1.id),
            "id": str(self.fixture.data_structure_json_1.id),
        }
        request = self.factory.post(
            "core_curate_app_json_text_editor_view", data
        )
        request.user = self.anonymous
        response = DataStructureJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 403)

    def test_user_save_json_content_returns_dne_error(self):
        """test_user_save_json_content_returns_dne_error

        Returns:

        """
        data = {
            "content": "{}",
            "action": "save",
            "document_id": "-1",
            "id": "-1",
        }
        request = self.factory.post(
            "core_curate_app_json_text_editor_view", data
        )
        request.user = self.user1
        response = DataStructureJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_save_json_content_returns_error(self):
        """test_user_save_json_content_returns_error

        Returns:

        """
        data = {
            "action": "save",
            "document_id": "-1",
            "id": "-1",
        }
        request = self.factory.post(
            "core_curate_app_json_text_editor_view", data
        )
        request.user = self.user1
        response = DataStructureJSONEditor.as_view()(request)
        self.assertEqual(response.status_code, 400)

    def test_user_save_invalid_json_content_returns_error(self):
        """test_user_save_invalid_json_content_returns_error

        Returns:

        """
        data = {
            "content": json.dumps({"$schema": "mock_schema"}),
            "action": "save",
            "document_id": str(self.fixture.data_structure_json_1.id),
            "id": str(self.fixture.data_structure_json_1.id),
        }
        request = self.factory.post(
            "core_curate_app_json_text_editor_view", data
        )
        setattr(request, "session", "session")
        messages = FallbackStorage(request)
        setattr(request, "_messages", messages)
        request.user = self.user1
        self.assertEqual(
            DataStructureJSONEditor.as_view()(request).status_code, 400
        )

    @patch("core_main_app.utils.file.get_byte_size_from_string")
    def test_json_content_too_big_returns_error(self, mock_get_byte_size):
        """test_json_content_too_big_returns_error

        Returns:

        """
        mock_get_byte_size.return_value = MAX_DOCUMENT_EDITING_SIZE + 1
        request = self.factory.get("core_curate_app_json_text_editor_view")
        request.GET = {"id": str(self.fixture.data_structure_json_1.id)}
        request.user = self.user1
        response = DataStructureJSONEditor.as_view()(request)
        self.assertTrue(
            "MAX_DOCUMENT_EDITING_SIZE" in response.content.decode()
        )
