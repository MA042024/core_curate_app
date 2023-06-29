""" Unit tests for views from `views.user.ajax`.
"""
from unittest import TestCase
from unittest.mock import patch, Mock

from django.http import HttpResponseBadRequest, HttpResponse
from django.test import RequestFactory

from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_curate_app.views.user import ajax as curate_user_ajax


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
    def test_curate_datastructure_delete_error_returns_http_bad_request(
        self, mock_curate_data_structure_api
    ):
        """test_curate_datastructure_delete_error_returns_http_bad_request"""
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

    @patch.object(curate_user_ajax, "messages")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_success_returns_http_response(
        self, mock_curate_data_structure_api, mock_messages
    ):
        """test_success_returns_http_response"""
        mock_curate_data_structure = Mock()
        mock_curate_data_structure.data = None
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        mock_curate_data_structure_api.delete.return_value = None
        mock_messages.add_message.return_value = None

        response = curate_user_ajax.cancel_form(self.request)
        self.assertIsInstance(response, HttpResponse)


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

    @patch.object(curate_user_ajax, "render_xml")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_render_xml_called(
        self, mock_curate_data_structure_api, mock_render_xml
    ):
        """test_render_xml_called"""
        mock_curate_data_structure = Mock()
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        curate_user_ajax.save_form(self.request)

        mock_render_xml.assert_called_with(
            self.request,
            mock_curate_data_structure.data_structure_element_root,
        )

    @patch.object(curate_user_ajax, "render_xml")
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

    @patch.object(curate_user_ajax, "render_xml")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_curate_data_structure_api_upsert_called(
        self, mock_curate_data_structure_api, mock_render_xml
    ):
        """test_curate_data_structure_api_upsert_called"""
        mock_curate_data_structure = Mock()
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        mock_render_xml.return_value = Mock()

        curate_user_ajax.save_form(self.request)

        mock_curate_data_structure_api.upsert.assert_called_with(
            mock_curate_data_structure, self.request.user
        )

    @patch.object(curate_user_ajax, "render_xml")
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

    @patch.object(curate_user_ajax, "render_xml")
    @patch.object(curate_user_ajax, "curate_data_structure_api")
    def test_success_returns_http_request(
        self, mock_curate_data_structure_api, mock_render_xml
    ):
        """test_success_returns_http_request"""
        mock_curate_data_structure = Mock()
        mock_curate_data_structure_api.get_by_id.return_value = (
            mock_curate_data_structure
        )
        mock_render_xml.return_value = Mock()
        mock_curate_data_structure_api.upsert.return_value = None

        response = curate_user_ajax.save_form(self.request)
        self.assertIsInstance(response, HttpResponse)
