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
        self.user2 = create_mock_user(user_id="3")
        self.fixture = DataStructureFixtures()
        self.fixture.insert_data()

    def test_xsd_template_start_curate_new_returns_http_200(self):
        """test_xsd_template_start_curate_new_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "new",
            "document_name": "test",
            "template_format": "XSD",
            "forms": "",
            "template_id": str(self.fixture.data_structure_1.template.id),
        }
        request = self.factory.post("core_curate_start", data)
        request.user = self.user1
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("/enter-data/" in response.content.decode("utf-8"))

    def test_xsd_template_start_curate_new_in_text_editor_returns_http_200(
        self,
    ):
        """test_xsd_template_start_curate_new_in_text_editor_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "new",
            "document_name": "test",
            "forms": "",
            "template_format": "XSD",
            "text_editor": "on",
            "template_id": str(self.fixture.data_structure_1.template.id),
        }
        request = self.factory.post("core_curate_start", data)
        request.user = self.user1
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ("/xml-editor/form" in response.content.decode("utf-8"))
        )

    def test_xsd_template_start_curate_upload_returns_http_200(self):
        """test_xsd_template_start_curate_upload_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "upload",
            "document_name": "",
            "template_format": "XSD",
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
        self.assertTrue(("/enter-data/" in response.content.decode("utf-8")))

    def test_xsd_template_start_curate_upload_bad_content_format_returns_error_400(
        self,
    ):
        """test_xsd_template_start_curate_upload_bad_content_format_returns_error_400

        Returns:

        """
        data = {
            "curate_form": "upload",
            "document_name": "",
            "template_format": "XSD",
            "forms": "",
            "template_id": str(self.fixture.data_structure_1.template.id),
        }
        content = "bad format"
        files = SimpleUploadedFile("test.xml", content.encode("utf-8"))

        request = self.factory.post("core_curate_start", data)
        request.FILES["file"] = files
        request.user = self.user1
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            (
                "the file is not well formed XSD"
                in response.content.decode("utf-8")
            )
        )

    def test_xsd_template_start_curate_in_text_editor_upload_returns_http_200(
        self,
    ):
        """test_xsd_template_start_curate_in_text_editor_upload_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "upload",
            "document_name": "",
            "template_format": "XSD",
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
        self.assertTrue(
            ("/xml-editor/form" in response.content.decode("utf-8"))
        )

    def test_xsd_template_start_curate_open_form_returns_http_200(self):
        """test_xsd_template_start_curate_open_form_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "open",
            "document_name": "test",
            "template_format": "XSD",
            "forms": str(self.fixture.data_structure_1.id),
            "template_id": str(self.fixture.data_structure_1.template.id),
        }
        request = self.factory.post("core_curate_start", data)
        request.user = self.user1
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(("/enter-data/" in response.content.decode("utf-8")))

    def test_xsd_template_start_curate_open_form_in_text_editor_returns_http_200(
        self,
    ):
        """test_xsd_template_start_curate_open_form_in_text_editor_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "open",
            "document_name": "test",
            "template_format": "XSD",
            "forms": str(self.fixture.data_structure_1.id),
            "text_editor": "on",
            "template_id": str(self.fixture.data_structure_1.template.id),
        }
        request = self.factory.post("core_curate_start", data)
        request.user = self.user1
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ("/xml-editor/form" in response.content.decode("utf-8"))
        )

    def test_json_template_start_curate_new_returns_http_200(self):
        """test_json_template_start_curate_new_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "new",
            "document_name": "test_json",
            "forms": "",
            "template_format": "JSON",
            "template_id": str(self.fixture.template_json.id),
        }
        request = self.factory.post("core_curate_start", data)
        request.user = self.user2
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue("/enter-data/" in response.content.decode("utf-8"))

    def test_json_template_start_curate_new_in_text_editor_returns_http_200(
        self,
    ):
        """test_json_template_start_curate_new_in_text_editor_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "new",
            "document_name": "test_json",
            "forms": "",
            "template_format": "JSON",
            "text_editor": "on",
            "template_id": str(self.fixture.template_json.id),
        }
        request = self.factory.post("core_curate_start", data)
        request.user = self.user2
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ("/json-editor/form" in response.content.decode("utf-8"))
        )

    def test_json_template_start_curate_upload_returns_http_200(self):
        """test_json_template_start_curate_upload_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "upload",
            "document_name": "",
            "template_format": "JSON",
            "forms": "",
            "text_editor": "on",
            "template_id": str(self.fixture.template_json.id),
        }
        content = "{}"
        files = SimpleUploadedFile("test_json.json", content.encode("utf-8"))

        request = self.factory.post("core_curate_start", data)
        request.FILES["file"] = files
        request.user = self.user2
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ("/json-editor/form" in response.content.decode("utf-8"))
        )

    def test_json_template_start_curate_upload_bad_content_format_returns_error_400(
        self,
    ):
        """test_json_template_start_curate_upload_bad_content_format_returns_error_400

        Returns:

        """
        data = {
            "curate_form": "upload",
            "document_name": "",
            "template_format": "JSON",
            "forms": "",
            "template_id": str(self.fixture.template_json.id),
        }
        content = "{ bad format"
        files = SimpleUploadedFile("test_json.json", content.encode("utf-8"))

        request = self.factory.post("core_curate_start", data)
        request.FILES["file"] = files
        request.user = self.user2
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            (
                "the file is not well formed JSON"
                in response.content.decode("utf-8")
            )
        )

    def test_json_template_start_curate_in_text_editor_upload_returns_http_200(
        self,
    ):
        """test_json_template_start_curate_in_text_editor_upload_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "upload",
            "document_name": "",
            "template_format": "JSON",
            "forms": "",
            "text_editor": "on",
            "template_id": str(self.fixture.template_json.id),
        }
        content = "{}"
        files = SimpleUploadedFile("test_json.json", content.encode("utf-8"))

        request = self.factory.post("core_curate_start", data)
        request.FILES["file"] = files
        request.user = self.user2
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ("/json-editor/form" in response.content.decode("utf-8"))
        )

    def test_json_template_start_curate_open_form_returns_http_200(self):
        """test_json_template_start_curate_open_form_returns_http_200

        Returns:

        """
        data = {
            "curate_form": "open",
            "document_name": "test_json",
            "template_format": "JSON",
            "text_editor": "on",
            "forms": str(self.fixture.data_structure_json_2.id),
            "template_id": str(self.fixture.template_json.id),
        }
        request = self.factory.post("core_curate_start", data)
        request.user = self.user2
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ("/json-editor/form" in response.content.decode("utf-8"))
        )

    def test_start_curate_upload_bad_format_returns_error_400(self):
        """test_start_curate_upload_bad_format_returns_error_400

        Returns:

        """
        data = {
            "curate_form": "upload",
            "document_name": "",
            "template_format": "BAD_FORMAT",
            "forms": "",
            "template_id": str(self.fixture.template_unsupported_format.id),
        }
        content = "test"
        files = SimpleUploadedFile("test.bad_format", content.encode("utf-8"))

        request = self.factory.post("core_curate_start", data)
        request.FILES["file"] = files
        request.user = self.user2
        response = curate_ajax._start_curate_post(request)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            "Template format not supported."
            in response.content.decode("utf-8")
        )
