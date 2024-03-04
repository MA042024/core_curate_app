""" Unit tests for views from `views.user.ajax`.
"""
import json
from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from django.http import HttpResponseBadRequest
from django.test import RequestFactory

from core_curate_app.components.curate_data_structure.models import (
    CurateDataStructure,
)
from core_curate_app.views.user import ajax as curate_user_ajax
from core_curate_app.views.user import views as curate_user_views
from core_main_app.commons.exceptions import DoesNotExist, JSONError
from core_main_app.components.template.models import Template
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestCancelChangesView(TestCase):
    """Unit tests for `cancel_changes` method."""

    def setUp(self):
        """setUp"""
        factory = RequestFactory()
        user1 = create_mock_user(user_id="1", has_perm=True)

        self.request = factory.get("core_curate_cancel_changes")
        self.request.POST = {"id": 1}
        self.request.user = user1

    @patch("core_curate_app.views.user.views.render_form")
    @patch("core_curate_app.views.user.views.generate_root_element")
    @patch("core_curate_app.components.curate_data_structure.api.get_by_id")
    def test_cancel_changes_return_http_response_with_xsd_form(
        self,
        mock_curate_data_structure_get_by_id,
        mock_generate_root_element,
        mock_render_form,
    ):
        """test_cancel_changes_return_http_response_with_xsd_form"""
        mock_data = MagicMock(
            data=None, form_string=None, template=_get_template()
        )
        mock_curate_data_structure_get_by_id.return_value = mock_data

        mock_generate_root_element.return_value = MagicMock()
        mock_render_form.return_value = "form"

        response = curate_user_ajax.cancel_changes(
            self.request,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("xsdForm", response.content.decode())

    @patch("core_curate_app.components.curate_data_structure.api.get_by_id")
    def test_cancel_changes_return_http_response_with_content(
        self,
        mock_curate_data_structure_get_by_id,
    ):
        """test_cancel_changes_return_http_response_with_content"""
        mock_data = MagicMock(
            form_string="test", data=None, template=_get_json_template()
        )
        mock_curate_data_structure_get_by_id.return_value = mock_data

        response = curate_user_ajax.cancel_changes(
            self.request,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("content", response.content.decode())

    @patch("core_curate_app.views.user.views.render_form")
    @patch("core_curate_app.views.user.views.generate_root_element")
    @patch("core_curate_app.components.curate_data_structure.api.get_by_id")
    def test_cancel_changes_with_empty_string_form_returns_http_200(
        self,
        mock_curate_data_structure_get_by_id,
        mock_generate_root_element,
        mock_render_form,
    ):
        """test_cancel_changes_with_empty_string_form_returns_http_200"""
        mock_data = MagicMock(template=_get_template())
        mock_curate_data_structure_get_by_id.return_value = mock_data

        mock_generate_root_element.return_value = MagicMock()
        mock_render_form.return_value = "form"

        response = curate_user_ajax.cancel_changes(
            self.request,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("xsdForm", response.content.decode())

    @patch("core_curate_app.views.user.views.render_form")
    @patch("core_curate_app.views.user.views.generate_root_element")
    @patch("core_curate_app.components.curate_data_structure.api.get_by_id")
    def test_cancel_changes_with_string_form_returns_http_200(
        self,
        mock_curate_data_structure_get_by_id,
        mock_generate_root_element,
        mock_render_form,
    ):
        """test_cancel_changes_with_empty_string_form_returns_http_200"""
        mock_data = MagicMock(string_form="test", template=_get_template())
        mock_curate_data_structure_get_by_id.return_value = mock_data

        mock_generate_root_element.return_value = MagicMock()
        mock_render_form.return_value = "form"

        response = curate_user_ajax.cancel_changes(
            self.request,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("xsdForm", response.content.decode())

    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_cancel_changes_returns_http_bad_request_when_template_format_is_not_supported(
        self, mock_curate_data_structure_api
    ):
        """test_cancel_changes_with_xsd_template_returns_http_200"""
        mock_curate_data_structure = Mock(
            template=Template(format="BAD_FORMAT")
        )
        mock_curate_data_structure.data = None
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        mock_curate_data_structure_api.delete.return_value = None

        response = curate_user_ajax.cancel_changes(self.request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Template format not supported.")


class TestCancelFormView(TestCase):
    """Unit tests for `cancel_form` method."""

    def setUp(self):
        """setUp"""
        factory = RequestFactory()
        user1 = create_mock_user(user_id="1", has_perm=True)

        self.request = factory.get("core_curate_cancel_form")
        self.request.POST = {"id": 1}
        self.request.user = user1

    def test_request_post_id_error_returns_http_bad_request(self):
        """test_request_post_id_error_returns_http_bad_request"""
        del self.request.POST["id"]
        response = curate_user_ajax.cancel_form(self.request)

        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_curate_data_structure_get_by_id_called(
        self, mock_curate_data_structure_api
    ):
        """test_curate_data_structure_get_by_id_called"""
        curate_user_ajax.cancel_form(self.request)
        mock_curate_data_structure_api.get_by_id.assert_called_with(
            self.request.POST["id"], self.request.user
        )

    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_curate_data_structure_get_by_id_error_returns_http_bad_request(
        self, mock_curate_data_structure_api
    ):
        """test_curate_data_structure_get_by_id_error_returns_http_bad_request"""
        mock_curate_data_structure_api.get_by_id.side_effect = Exception(
            "mock_get_by_id_exception"
        )
        response = curate_user_ajax.cancel_form(self.request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(curate_user_ajax, "lock_api")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_data_locked_if_data_linked_to_curate_data_structure(
        self, mock_curate_data_structure_api, mock_lock_api
    ):
        """test_data_locked_if_data_linked_to_curate_data_structure"""
        mock_curate_data_structure = Mock()
        mock_curate_data_structure.data = Mock()
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        curate_user_ajax.cancel_form(self.request)

        mock_lock_api.remove_lock_on_object.assert_called_with(
            mock_curate_data_structure.data, self.request.user
        )

    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_curate_datastructure_delete_called(
        self, mock_curate_data_structure_api
    ):
        """test_curate_datastructure_delete_called"""
        mock_curate_data_structure = Mock()
        mock_curate_data_structure.data = None
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        curate_user_ajax.cancel_form(self.request)

        mock_curate_data_structure_api.delete.assert_called_with(
            mock_curate_data_structure, self.request.user
        )

    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_curate_data_structure_delete_error_returns_http_bad_request(
        self, mock_curate_data_structure_api
    ):
        """test_curate_data_structure_delete_error_returns_http_bad_request"""
        mock_curate_data_structure = Mock()
        mock_curate_data_structure.data = None
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        mock_curate_data_structure_api.delete.side_effect = Exception(
            "mock_delete_exception"
        )

        response = curate_user_ajax.cancel_form(self.request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(curate_user_ajax, "messages")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_add_message_called(
        self, mock_curate_data_structure_api, mock_messages
    ):
        """test_add_message_called"""
        mock_curate_data_structure = Mock()
        mock_curate_data_structure.data = None
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        mock_curate_data_structure_api.delete.return_value = None

        curate_user_ajax.cancel_form(self.request)
        mock_messages.add_message.assert_called()


class TestSaveFormView(TestCase):
    """Unit tests for `save_form` method."""

    def setUp(self):
        """setUp"""
        factory = RequestFactory()
        user1 = create_mock_user(user_id="1", has_perm=True)

        self.request = factory.get("core_curate_save_form")
        self.request.POST = {"id": 1}
        self.request.user = user1

    def test_request_post_id_error_returns_http_bad_request(self):
        """test_request_post_id_error_returns_http_bad_request"""
        del self.request.POST["id"]

        response = curate_user_ajax.save_form(self.request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_curate_data_structure_api_get_by_id_called(
        self, mock_curate_data_structure_api
    ):
        """test_curate_data_structure_api_get_by_id_called"""
        curate_user_ajax.save_form(self.request)

        mock_curate_data_structure_api.get_by_id.assert_called_with(
            self.request.POST["id"], self.request.user
        )

    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_curate_data_structure_api_get_by_id_error_returns_http_bad_request(
        self, mock_curate_data_structure_api
    ):
        """test_curate_data_structure_api_get_by_id_error_returns_http_bad_request"""
        mock_curate_data_structure_api.get_by_id.side_effect = Exception(
            "mock_get_by_id_exception"
        )

        response = curate_user_ajax.save_form(self.request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(curate_user_views, "render_xml")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_render_xml_called(
        self, mock_curate_data_structure_api, mock_render_xml
    ):
        """test_render_xml_called"""
        mock_curate_data_structure = CurateDataStructure(
            form_string="text", template=Template(format=Template.XSD)
        )
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        curate_user_ajax.save_form(self.request)

        mock_render_xml.assert_called_with(
            self.request,
            mock_curate_data_structure.data_structure_element_root,
        )

    @patch.object(curate_user_views, "render_xml")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_render_xml_error_returns_http_bad_request(
        self, mock_curate_data_structure_api, mock_render_xml
    ):
        """test_render_xml_error_returns_http_bad_request"""
        mock_curate_data_structure = Mock()
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        mock_render_xml.side_effect = Exception("mock_render_xml_exception")

        response = curate_user_ajax.save_form(self.request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(curate_user_views, "render_xml")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_curate_data_structure_api_upsert_called(
        self, mock_curate_data_structure_api, mock_render_xml
    ):
        """test_curate_data_structure_api_upsert_called"""
        mock_curate_data_structure = CurateDataStructure(
            form_string="text", template=Template(format=Template.XSD)
        )
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        mock_render_xml.return_value = Mock()

        curate_user_ajax.save_form(self.request)

        mock_curate_data_structure_api.upsert.assert_called_with(
            mock_curate_data_structure, self.request.user
        )

    @patch.object(curate_user_views, "render_xml")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_curate_data_structure_api_upsert_error_returns_http_bad_request(
        self, mock_curate_data_structure_api, mock_render_xml
    ):
        """test_curate_data_structure_api_upsert_error_returns_http_bad_request"""
        mock_curate_data_structure = Mock()
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        mock_render_xml.return_value = Mock()
        mock_curate_data_structure_api.upsert.side_effect = Exception(
            "mock_upsert_exception"
        )

        response = curate_user_ajax.save_form(self.request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(curate_user_views, "render_xml")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_save_form_with_xsd_template_returns_http_200(
        self, mock_curate_data_structure_api, mock_render_xml
    ):
        """test_save_form_with_xsd_template_returns_http_200"""
        mock_template = _get_template()
        mock_curate_data_structure_api.get_by_id.return_value = MagicMock(
            template=mock_template, data=None, name="title"
        )
        mock_render_xml.return_value = Mock()
        mock_curate_data_structure_api.upsert.return_value = None

        response = curate_user_ajax.save_form(self.request)
        self.assertEqual(response.status_code, 200)

    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_save_form_with_json_template_returns_http_200(
        self, mock_curate_data_structure_api
    ):
        """test_save_form_with_json_template_returns_http_200"""
        mock_template = _get_json_template()
        mock_curate_data_structure_api.get_by_id.return_value = MagicMock(
            template=mock_template, data=None, name="title"
        )
        mock_curate_data_structure_api.upsert.return_value = None

        response = curate_user_ajax.save_form(self.request)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "saved with success." in response.content.decode("utf-8")
        )

    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_save_form_with_well_formed_content_returns_http_200(
        self, mock_curate_data_structure_api
    ):
        """test_save_form_with_well_formed_content_returns_http_200"""
        mock_curate_data_structure = CurateDataStructure(
            form_string="text", template=Template(format=Template.XSD)
        )
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        self.request.POST = {"id": 1, "form_string": "<text></text>"}
        response = curate_user_ajax.save_form(self.request)
        self.assertEqual(response.status_code, 200)

    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_save_form_with_not_well_formed_content_returns_error(
        self, mock_curate_data_structure_api
    ):
        """test_save_form_with_not_well_formed_content_returns_error"""
        mock_curate_data_structure = CurateDataStructure(
            form_string="text", template=Template(format=Template.XSD)
        )
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        self.request.POST = {"id": 1, "form_string": "</text>"}
        response = curate_user_ajax.save_form(self.request)
        self.assertEqual(response.status_code, 400)
        self.assertTrue(
            "Content is not well formatted XML." in response.content.decode()
        )


class TestGenerateChoiceView(TestCase):
    """Unit tests for the `generate_choice` method."""

    def setUp(self):
        """setUp"""
        factory = RequestFactory()
        user1 = create_mock_user(user_id="1", has_perm=True)

        self.request = factory.get("core_curate_generate_choice")
        self.request.POST = {"id": 1}
        self.request.user = user1

    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_generate_choice_return_http_bad_request_if_not_xsd_template(
        self, mock_curate_data_structure_api, mock_template_get_by_id
    ):
        """test_generate_choice_return_http_bad_request_if_not_xsd_template"""
        mock_template = _get_json_template()
        mock_curate_data_structure_api.return_value = MagicMock(
            template=mock_template
        )
        mock_template_get_by_id.return_value = mock_template

        response = curate_user_ajax.generate_choice(
            self.request, curate_data_structure_id=1
        )

        self.assertTrue(mock_template_get_by_id.called)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Template format not supported.")

    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_generate_choice_with_error_returns_http_bad_request(
        self, mock_curate_data_structure_api
    ):
        """test_generate_choice_with_error_returns_http_bad_request"""
        mock_curate_data_structure_api.side_effect = DoesNotExist("error")

        response = curate_user_ajax.generate_choice(
            self.request, curate_data_structure_id=1
        )

        self.assertEqual(response.status_code, 400)

    @patch(
        "core_parser_app.tools.parser.parser.XSDParser.generate_choice_absent"
    )
    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_generate_choice_returns_html_form(
        self,
        mock_curate_data_structure_api,
        mock_template_get_by_id,
        mock_generate_choice_absent,
    ):
        """test_generate_choice_returns_html_form"""
        mock_template = _get_template()
        mock_curate_data_structure_api.return_value = MagicMock(
            template=mock_template
        )
        mock_template_get_by_id.return_value = mock_template
        mock_generate_choice_absent.return_value = "form"

        response = curate_user_ajax.generate_choice(
            self.request, curate_data_structure_id=1
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"form")


class TestGenerateElementView(TestCase):
    """Unit tests for `generate_element` method."""

    def setUp(self):
        """setUp"""
        factory = RequestFactory()
        user1 = create_mock_user(user_id="1", has_perm=True)

        self.request = factory.get("core_curate_generate_element")
        self.request.POST = {"id": 1}
        self.request.user = user1

    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_generate_element_return_http_bad_request_if_not_xsd_template(
        self, mock_curate_data_structure_api, mock_template_get_by_id
    ):
        """test_generate_element_return_http_bad_request_if_not_xsd_template"""
        mock_template = _get_json_template()
        mock_curate_data_structure_api.return_value = MagicMock(
            template=mock_template
        )
        mock_template_get_by_id.return_value = mock_template

        response = curate_user_ajax.generate_element(
            self.request, curate_data_structure_id=1
        )

        self.assertTrue(mock_template_get_by_id.called)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Template format not supported.")

    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_generate_element_with_error_returns_http_bad_request(
        self, mock_curate_data_structure_api
    ):
        """test_generate_element_with_error_returns_http_bad_request"""
        mock_curate_data_structure_api.side_effect = DoesNotExist("error")

        response = curate_user_ajax.generate_element(
            self.request, curate_data_structure_id=1
        )

        self.assertEqual(response.status_code, 400)

    @patch(
        "core_parser_app.tools.parser.parser.XSDParser.generate_element_absent"
    )
    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_generate_element_returns_html_form(
        self,
        mock_curate_data_structure_api,
        mock_template_get_by_id,
        mock_generate_choice_absent,
    ):
        """test_generate_element_returns_html_form"""
        mock_template = _get_template()
        mock_curate_data_structure_api.return_value = MagicMock(
            template=mock_template
        )
        mock_template_get_by_id.return_value = mock_template
        mock_generate_choice_absent.return_value = "form"

        response = curate_user_ajax.generate_element(
            self.request, curate_data_structure_id=1
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"form")


class TestClearFieldsView(TestCase):
    """Unit tests for `clear_fields` method."""

    def setUp(self):
        """setUp"""
        factory = RequestFactory()
        user1 = create_mock_user(user_id="1", has_perm=True)

        self.request = factory.get("core_curate_generate_element")
        self.request.POST = {"id": 1}
        self.request.user = user1

    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_clear_fields_return_http_bad_request_if_not_xsd_template(
        self, mock_curate_data_structure_api, mock_template_get_by_id
    ):
        """test_clear_fields_return_http_bad_request_if_not_xsd_template"""
        mock_template = _get_json_template()
        mock_curate_data_structure_api.return_value = MagicMock(
            template=mock_template
        )
        mock_template_get_by_id.return_value = mock_template

        response = curate_user_ajax.clear_fields(
            self.request,
        )

        self.assertTrue(mock_template_get_by_id.called)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Template format not supported.")

    @patch("core_curate_app.views.user.views.render_form")
    @patch("core_curate_app.views.user.views.generate_form")
    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_clear_fields_returns_form(
        self,
        mock_curate_data_structure_api,
        mock_template_get_by_id,
        mock_generate_form,
        mock_render_form,
    ):
        """test_clear_fields_returns_form"""
        mock_template = _get_template()
        mock_curate_data_structure_api.return_value = MagicMock(
            template=mock_template
        )
        mock_template_get_by_id.return_value = mock_template
        mock_generate_form.return_value = MagicMock()
        mock_render_form.return_value = "form"

        response = curate_user_ajax.clear_fields(
            self.request,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("xsdForm", response.content.decode())


class TestValidateFormView(TestCase):
    """Unit tests for `validate_form` method."""

    def setUp(self):
        """setUp"""
        factory = RequestFactory()
        user1 = create_mock_user(user_id="1", has_perm=True)

        self.request = factory.get("core_curate_validate_form")
        self.request.POST = {"id": 1}
        self.request.user = user1

    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_validate_form_returns_http_bad_request_when_template_is_not_supported(
        self, mock_curate_data_structure_api, mock_template_get_by_id
    ):
        """test_validate_form_return_http_bad_request_when_template_is_not_supported"""
        mock_template = _get_json_template()
        mock_template.format = "mock_unsupported_format"
        mock_curate_data_structure_api.return_value = MagicMock(
            template=mock_template
        )
        mock_template_get_by_id.return_value = mock_template

        response = curate_user_ajax.validate_form(
            self.request,
        )

        self.assertTrue(mock_template_get_by_id.called)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Template format not supported.")

    @patch.object(curate_user_views, "render_xml")
    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_validate_form_returns_errors(
        self,
        mock_curate_data_structure_api,
        mock_template_get_by_id,
        mock_render_xml,
    ):
        """test_validate_form_returns_errors"""
        mock_template = _get_template()
        mock_curate_data_structure_api.return_value = MagicMock(
            template=mock_template
        )
        mock_template_get_by_id.return_value = mock_template
        mock_render_xml.return_value = "<root></root>"

        response = curate_user_ajax.validate_form(
            self.request,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("errors", response.content.decode())

    @patch.object(curate_user_ajax, "main_json_utils")
    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_validate_json_form_calls_validate_json_data(
        self,
        mock_curate_data_structure_api,
        mock_template_get_by_id,
        mock_json_utils,
    ):
        """test_validate_json_form_calls_validate_json_data"""
        mock_template = _get_json_template()
        mock_curate_data_structure = MagicMock(
            template=mock_template, form_string=json.dumps({"root": "value"})
        )
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        mock_template_get_by_id.return_value = mock_template

        curate_user_ajax.validate_form(
            self.request,
        )

        mock_json_utils.validate_json_data.assert_called_with(
            mock_curate_data_structure.form_string, mock_template.content
        )

    @patch.object(curate_user_ajax, "main_json_utils")
    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_invalid_json_form_returns_errors(
        self,
        mock_curate_data_structure_api,
        mock_template_get_by_id,
        mock_json_utils,
    ):
        """test_invalid_json_form_returns_errors"""
        mock_template = _get_json_template()
        mock_curate_data_structure = MagicMock(
            template=mock_template, form_string=json.dumps({"root": "value"})
        )
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        mock_template_get_by_id.return_value = mock_template
        mock_json_errors = ["error1", "error2"]
        mock_json_utils.validate_json_data.side_effect = JSONError(
            mock_json_errors
        )

        response = curate_user_ajax.validate_form(
            self.request,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content), {"errors": mock_json_errors}
        )

    @patch.object(curate_user_ajax, "main_json_utils")
    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_valid_json_form_returns_empty(
        self,
        mock_curate_data_structure_api,
        mock_template_get_by_id,
        mock_json_utils,
    ):
        """test_invalid_json_form_returns_errors"""
        mock_template = _get_json_template()
        mock_curate_data_structure = MagicMock(
            template=mock_template, form_string=json.dumps({"root": "value"})
        )
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        mock_template_get_by_id.return_value = mock_template
        mock_json_utils.validate_json_data.return_value = None

        response = curate_user_ajax.validate_form(
            self.request,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {})


class TestSaveDataView(TestCase):
    """Unit tests for `save_data` method."""

    def setUp(self):
        """setUp"""
        factory = RequestFactory()
        user1 = create_mock_user(user_id="1", has_perm=True)

        self.request = factory.get("core_curate_save_data")
        self.request.POST = {"id": 1}
        self.request.user = user1

    @patch.object(curate_user_ajax, "messages")
    @patch("core_main_app.components.data.api.upsert")
    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_views, "render_xml")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_save_data_returns_http_response_if_xsd_template(
        self,
        mock_curate_data_structure_api,
        mock_render_xml,
        mock_template_get_by_id,
        mock_data_upsert,
        mock_messages,
    ):
        """test_save_data_returns_http_response_if_xsd_template"""
        mock_template = _get_template()
        mock_curate_data_structure_api.get_by_id.return_value = MagicMock(
            template=mock_template, data=None, name="title"
        )
        mock_curate_data_structure_api.delete.return_value = None
        mock_render_xml.return_value = "<root></root>"
        mock_template_get_by_id.return_value = mock_template
        mock_data_upsert.return_value = MagicMock(id=1)

        response = curate_user_ajax.save_data(
            self.request,
        )

        self.assertTrue(mock_curate_data_structure_api.get_by_id.called)
        self.assertTrue(mock_curate_data_structure_api.delete.called)
        self.assertTrue(mock_template_get_by_id.called)
        self.assertTrue(mock_data_upsert.called)
        self.assertEqual(response.status_code, 200)

    @patch.object(curate_user_ajax, "messages")
    @patch("core_main_app.components.data.api.upsert")
    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_save_data_returns_http_response_if_json_template(
        self,
        mock_curate_data_structure_api,
        mock_template_get_by_id,
        mock_data_upsert,
        mock_messages,
    ):
        """test_save_data_returns_http_response_if_json_template"""
        mock_template = _get_json_template()
        mock_curate_data_structure_api.get_by_id.return_value = MagicMock(
            template=mock_template, data=None, name="title"
        )
        mock_curate_data_structure_api.delete.return_value = None
        mock_template_get_by_id.return_value = mock_template
        mock_data_upsert.return_value = MagicMock(id=1)

        response = curate_user_ajax.save_data(
            self.request,
        )

        self.assertTrue(mock_curate_data_structure_api.get_by_id.called)
        self.assertTrue(mock_curate_data_structure_api.delete.called)
        self.assertTrue(mock_template_get_by_id.called)
        self.assertTrue(mock_data_upsert.called)
        self.assertEqual(response.status_code, 200)

    @patch.object(curate_user_ajax, "messages")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_save_data_returns_http_bad_request_when_template_is_not_supported(
        self,
        mock_curate_data_structure_api,
        mock_messages,
    ):
        """test_save_data_returns_http_bad_request_when_template_is_not_supported"""
        mock_curate_data_structure_api.get_by_id.return_value = MagicMock(
            template=Template(format="BAD_FORMAT"), data=None, name="title"
        )
        mock_curate_data_structure_api.delete.return_value = None

        response = curate_user_ajax.save_data(
            self.request,
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Template format not supported.")


class TestStartCurateGetView(TestCase):
    """Unit tests for `_start_curate_get` method."""

    def setUp(self):
        """setUp"""
        factory = RequestFactory()
        user1 = create_mock_user(user_id="1", has_perm=True)

        self.request = factory.get("core_curate_start")
        self.request.GET = {"template_id": 1}
        self.request.user = user1

    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_start_curate_get_returns_http_response(
        self, mock_curate_data_structure_api, mock_template_get_by_id
    ):
        """test_start_curate_get_returns_http_response"""
        mock_template = _get_template()
        mock_curate_data_structure_api.get_all_by_user_id_and_template_id_with_no_data.return_value = MagicMock(
            template=mock_template,
        )
        mock_curate_data_structure_api.delete.return_value = None
        mock_template_get_by_id.return_value = mock_template

        response = curate_user_ajax._start_curate_get(
            self.request,
        )

        self.assertEqual(response.status_code, 200)


class TestStartCuratePostView(TestCase):
    """Unit tests for `_start_curate_post` method."""

    def setUp(self):
        """setUp"""
        factory = RequestFactory()
        user1 = create_mock_user(user_id="1", has_perm=True)

        self.request = factory.post("core_curate_start", {"file": Mock()})
        self.request.POST = {
            "template_id": 1,
            "curate_form": "new",
            "template_format": "XSD",
            "document_name": "test",
        }
        self.request.user = user1

    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_start_curate_post_returns_http_bad_response_when_bad_template_format(
        self, mock_curate_data_structure_api, mock_template_get_by_id
    ):
        """test_start_curate_post_returns_http_bad_response_when_bad_template_format"""
        mock_template = Template(format=None)
        mock_curate_data_structure_api.get_all_by_user_id_and_template_id_with_no_data.return_value = MagicMock(
            template=mock_template,
        )
        mock_curate_data_structure_api.delete.return_value = None
        mock_template_get_by_id.return_value = mock_template

        response = curate_user_ajax._start_curate_post(
            self.request,
        )

        self.assertTrue(mock_template_get_by_id.called)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, b"Template format not supported.")

    @patch.object(curate_user_ajax, "messages")
    @patch("core_main_app.components.data.api.upsert")
    @patch("core_main_app.views.common.views.read_xsd_file")
    @patch("core_main_app.utils.xml.is_well_formed_xml")
    @patch("core_main_app.components.template.api.get_by_id")
    def test_start_curate_post_upload_returns_http_response(
        self,
        mock_template_get_by_id,
        mock_is_well_formed,
        mock_read_xsd_file,
        mock_data_upsert,
        mock_messages,
    ):
        """test_start_curate_get_returns_http_response"""
        self.request.POST["curate_form"] = "upload"
        self.request.POST["direct_upload"] = True
        mock_template = _get_template()
        mock_template_get_by_id.return_value = mock_template
        mock_is_well_formed.return_value = True
        mock_read_xsd_file.return_value = "<root></root>"
        mock_data_upsert.return_value = None

        response = curate_user_ajax._start_curate_post(
            self.request,
        )

        self.assertEqual(response.status_code, 200)


def _get_json_template():
    """Get JSON template

    Returns:

    """
    template = Template()
    template.format = Template.JSON
    template.id_field = 1
    template.content = "{}"
    return template


def _get_template():
    """Get XSD template

    Returns:

    """
    template = Template()
    template.id_field = 1
    xsd = (
        '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
        '<xs:element name="tag"></xs:element></xs:schema>'
    )
    template.content = xsd
    template.format = Template.XSD
    return template
