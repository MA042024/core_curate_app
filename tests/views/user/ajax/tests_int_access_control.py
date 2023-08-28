""" Test access to views from `views.user.ajax`.
"""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import RequestFactory

from core_curate_app.views.user import ajax as curate_ajax
from core_main_app.utils.integration_tests.integration_base_test_case import (
    IntegrationBaseTestCase,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests.components.curate_data_structure.fixtures.fixtures import (
    DataStructureFixtures,
)

fixture_data_structure = DataStructureFixtures()


class TestStartCuratePost(IntegrationBaseTestCase):
    """Test Start Curate Post"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.fixture = DataStructureFixtures()
        self.fixture.insert_data()

    def test_start_curate_new_returns_http_200(self):
        """test_start_curate_new_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "new",
            "document_name": "test",
            "forms": "",
            "template_id": str(self.fixture.data_structure_1.template.id),
        }
        request = self.factory.post("core_curate_start", data)
        request.user = self.user1
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 200)

    def test_start_curate_new_in_text_editor_returns_http_200(self):
        """test_start_curate_new_in_text_editor_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "new",
            "document_name": "test",
            "forms": "",
            "text_editor": "on",
            "template_id": str(self.fixture.data_structure_1.template.id),
        }
        request = self.factory.post("core_curate_start", data)
        request.user = self.user1
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 200)

    def test_start_curate_upload_returns_http_200(self):
        """test_start_curate_upload_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "upload",
            "document_name": "",
            "forms": "",
            "template_id": str(self.fixture.data_structure_1.template.id),
        }
        content = "<tag></tag>"
        files = SimpleUploadedFile("test.xml", content.encode("utf-8"))

        request = self.factory.post("core_curate_start", data)
        request.FILES["file"] = files
        request.user = self.user1
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 200)

    def test_start_curate_in_text_editor_upload_returns_http_200(self):
        """test_start_curate_in_text_editor_upload_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "upload",
            "document_name": "",
            "forms": "",
            "text_editor": "on",
            "template_id": str(self.fixture.data_structure_1.template.id),
        }
        content = "<tag></tag>"
        files = SimpleUploadedFile("test.xml", content.encode("utf-8"))

        request = self.factory.post("core_curate_start", data)
        request.FILES["file"] = files
        request.user = self.user1
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 200)

    def test_start_curate_open_form_returns_http_200(self):
        """test_start_curate_open_form_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "open",
            "document_name": "test",
            "forms": str(self.fixture.data_structure_1.id),
            "template_id": str(self.fixture.data_structure_1.template.id),
        }
        request = self.factory.post("core_curate_start", data)
        request.user = self.user1
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 200)

    def test_start_curate_open_form_in_text_editor_returns_http_200(self):
        """test_start_curate_open_form_in_text_editor_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "open",
            "document_name": "test",
            "forms": str(self.fixture.data_structure_1.id),
            "text_editor": "on",
            "template_id": str(self.fixture.data_structure_1.template.id),
        }
        request = self.factory.post("core_curate_start", data)
        request.user = self.user1
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 200)
