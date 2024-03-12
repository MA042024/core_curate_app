""" Unit tests for views from `views.user.views`.
"""
from unittest.case import TestCase
from unittest.mock import patch, MagicMock

from django.http import (
    HttpResponseRedirect,
)
from django.test import RequestFactory, override_settings
from django.urls import reverse

from core_curate_app.views.user.views import (
    EnterDataView,
    ViewDataView,
    generate_root_element,
)
from core_curate_app.views.user import views as curate_user_views
from core_main_app.commons.exceptions import XSDError
from core_main_app.components.template.models import Template
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.xml import format_content_xml
from core_parser_app.tools.parser.exceptions import ParserError


class TestEnterDataView(TestCase):
    """Test EnterDataView"""

    def setUp(self):
        """setUp
        Returns:
        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.user1.has_perm = MagicMock()
        self.user1.has_perm.return_value = True

    @patch("core_curate_app.views.user.views.EnterDataView.build_context")
    @patch("core_curate_app.views.user.views._get_curate_data_structure_by_id")
    def test_enter_data_view_get_returns_error_if_parser_error_occurs(
        self, mock_ds_get_by_id, mock_build_context
    ):
        """test_enter_data_view_get_returns_error_if_parser_error_occurs"""
        # Arrange
        mock_build_context.side_effect = ParserError("error")
        mock_ds = MagicMock()
        mock_ds.form_string = "test"
        mock_ds.data = None
        mock_ds_get_by_id.return_value = mock_ds
        request = self.factory.get("core_curate_enter_data")
        request._messages = MagicMock()
        request.user = self.user1
        # Act
        response = EnterDataView.as_view()(request, curate_data_structure_id=1)
        # Assert
        self.assertTrue(isinstance(response, HttpResponseRedirect))
        self.assertTrue(
            response.url.startswith(
                reverse("core_curate_app_xml_text_editor_view")
            )
        )

    @override_settings(ENABLE_XML_ENTITIES_TOOLTIPS=True)
    def test_enable_xml_entities_tootip_true_includes_base_js_asset(self):
        """test_enable_xml_entities_tootip_true_includes_base_js_asset"""
        result = EnterDataView()

        self.assertIn(
            {
                "path": "core_curate_app/user/js/xml_entities_tooltip.js",
                "is_raw": False,
            },
            result.assets["js"],
        )

    @override_settings(ENABLE_XML_ENTITIES_TOOLTIPS=False)
    def test_enable_xml_entities_tootip_false_includes_no_extra_js(self):
        """test_enable_xml_entities_tootip_false_includes_no_extra_js"""
        result = EnterDataView()

        self.assertNotIn(
            {
                "path": "core_curate_app/user/js/xml_entities_tooltip.js",
                "is_raw": False,
            },
            result.assets["js"],
        )

    @override_settings(BOOTSTRAP_VERSION="4.6.2")
    def test_bootstrap_4_6_2_includes_correct_tooltip_js_asset(self):
        """test_bootstrap_4_6_2_includes_correct_tooltip_js_asset"""
        result = EnterDataView()

        self.assertIn(
            {
                "path": "core_curate_app/user/js/xml_entities_tooltip/popover.bs4.js",
                "is_raw": False,
            },
            result.assets["js"],
        )

    @override_settings(BOOTSTRAP_VERSION="5.1.3")
    def test_bootstrap_5_1_3_includes_correct_tooltip_js_asset(self):
        """test_bootstrap_5_1_3_includes_correct_tooltip_js_asset"""
        result = EnterDataView()

        self.assertIn(
            {
                "path": "core_curate_app/user/js/xml_entities_tooltip/popover.bs5.js",
                "is_raw": False,
            },
            result.assets["js"],
        )

    @patch.object(curate_user_views, "render_form")
    @patch("core_curate_app.views.user.views.generate_root_element")
    @patch("core_curate_app.views.user.views._get_curate_data_structure_by_id")
    def test_enter_data_view_build_context_with_xsd_template_returns_http_200(
        self, mock_ds_get_by_id, mock_generate_root_element, mock_render_form
    ):
        """test_enter_data_view_build_context_with_xsd_template_returns_http_200"""
        # Arrange
        mock_ds = MagicMock()
        mock_ds.form_string = "<root></root>"
        mock_ds.data = None
        mock_ds.template = Template(format=Template.XSD)
        mock_ds_get_by_id.return_value = mock_ds
        request = self.factory.get("core_curate_enter_data")
        request._messages = MagicMock()
        request.user = self.user1
        mock_generate_root_element.return_value = None
        mock_render_form.return_value = None
        # Act
        response = EnterDataView.as_view()(request, curate_data_structure_id=1)
        # Assert
        self.assertEqual(response.status_code, 200)

    @patch.object(curate_user_views, "render_form")
    @patch("core_curate_app.views.user.views.generate_root_element")
    @patch("core_curate_app.views.user.views._get_curate_data_structure_by_id")
    def test_enter_data_view_build_context_with_unsaved_changes_returns_http_200(
        self, mock_ds_get_by_id, mock_generate_root_element, mock_render_form
    ):
        """test_enter_data_view_build_context_with_unsaved_changes_returns_http_200"""
        # Arrange
        mock_ds = MagicMock()
        mock_ds.form_string = "<root></root>"
        mock_ds.data = None
        mock_ds.template = Template(format=Template.XSD)
        mock_ds_get_by_id.return_value = mock_ds
        request = self.factory.get("core_curate_enter_data")
        request._messages = MagicMock()
        request.user = self.user1
        mock_generate_root_element.return_value = None
        mock_render_form.return_value = None
        # Act
        response = EnterDataView.as_view()(
            request, curate_data_structure_id=1, reload_unsaved_changes=True
        )
        # Assert
        self.assertEqual(response.status_code, 200)

    @patch.object(curate_user_views, "render")
    @patch.object(curate_user_views, "render_form")
    @patch("core_curate_app.views.user.views.generate_root_element")
    @patch("core_curate_app.views.user.views._get_curate_data_structure_by_id")
    def test_enter_data_xml_includes_no_extra_css(
        self,
        mock_ds_get_by_id,
        mock_generate_root_element,
        mock_render_form,
        mock_render,
    ):
        """test_enter_data_xml_includes_no_extra_css"""
        mock_ds = MagicMock()
        mock_ds.form_string = "test"
        mock_ds.template = Template(format=Template.XSD)
        mock_ds.data = None
        mock_ds_get_by_id.return_value = mock_ds
        request = self.factory.get("core_curate_enter_data")
        request._messages = MagicMock()
        request.user = self.user1
        mock_generate_root_element.return_value = None
        mock_render_form.return_value = None
        expected_context = {
            "edit": False,
            "form": None,
            "data_structure": mock_ds,
            "page_title": "Enter Data",
        }
        # Act
        EnterDataView.as_view()(request, curate_data_structure_id=2)

        # Assert
        mock_render.assert_called_with(
            request,
            "core_curate_app/user/data-entry/enter_data.html",
            **{
                "assets": {
                    "js": [
                        {
                            "path": "core_main_app/common/js/debounce.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_main_app/common/js/elementViewport.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_curate_app/user/js/enter_data.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_curate_app/user/js/enter_data.raw.js",
                            "is_raw": True,
                        },
                        {
                            "path": "core_parser_app/js/modules.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_parser_app/js/modules.raw.js",
                            "is_raw": True,
                        },
                        {
                            "path": "core_main_app/common/js/XMLTree.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_parser_app/js/autosave.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_parser_app/js/autosave.raw.js",
                            "is_raw": True,
                        },
                        {
                            "path": "core_parser_app/js/buttons.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_curate_app/user/js/buttons.raw.js",
                            "is_raw": True,
                        },
                        {
                            "path": "core_parser_app/js/choice.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_curate_app/user/js/choice.raw.js",
                            "is_raw": True,
                        },
                        {
                            "path": "core_main_app/common/js/data_detail.js",
                            "is_raw": False,
                        },
                        {
                            "path": "https://cdnjs.cloudflare.com/ajax/libs/json-editor/2.14.1/jsoneditor.js",
                            "integrity": "sha512-G93wD4PAiaCg3T4BeJGXNUdwJ4jr6WL0dKUqz0UwZs0jVad7FnJ2r+SlJ50k6+ILkYcQBqt4M5YoFcBWujIH0A==",
                            "is_external": True,
                            "is_raw": False,
                        },
                        {
                            "path": "core_curate_app/user/js/xml_entities_tooltip.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_curate_app/user/js/xml_entities_tooltip/popover.bs4.js",
                            "is_raw": False,
                        },
                    ],
                    "css": [
                        "core_curate_app/user/css/common.css",
                        "core_curate_app/user/css/xsd_form.css",
                        "core_parser_app/css/use.css",
                        "core_main_app/common/css/modals/download.css",
                    ],
                },
                "context": expected_context,
                "modals": [
                    "core_curate_app/user/data-entry/modals/cancel-changes.html",
                    "core_curate_app/user/data-entry/modals/cancel-form.html",
                    "core_curate_app/user/data-entry/modals/clear-fields.html",
                    "core_main_app/common/modals/download-options.html",
                    "core_curate_app/user/data-entry/modals/save-form.html",
                    "core_curate_app/user/data-entry/modals/use-validation.html",
                    "core_curate_app/user/data-entry/modals/validation-error.html",
                    "core_curate_app/user/data-entry/modals/xml-valid.html",
                    "core_curate_app/user/data-entry/modals/switch_to_text_editor.html",
                ],
            },
        )

    @patch("core_curate_app.views.user.views._get_curate_data_structure_by_id")
    def test_enter_data_view_build_context_with_json_template_returns_http_200(
        self, mock_ds_get_by_id
    ):
        """test_enter_data_view_build_context_with_json_template_returns_http_200"""
        # Arrange
        mock_ds = MagicMock()
        mock_ds.form_string = "test"
        mock_ds.template = Template(format=Template.JSON)
        mock_ds.data = None
        mock_ds_get_by_id.return_value = mock_ds
        request = self.factory.get("core_curate_enter_data")
        request._messages = MagicMock()
        request.user = self.user1
        # Act
        response = EnterDataView.as_view()(request, curate_data_structure_id=1)
        # Assert
        self.assertEqual(response.status_code, 200)

    @patch.object(curate_user_views, "render")
    @patch("core_curate_app.views.user.views._get_curate_data_structure_by_id")
    def test_enter_data_json_includes_extra_css(
        self, mock_ds_get_by_id, mock_render
    ):
        """test_enter_data_json_includes_extra_css"""
        mock_ds = MagicMock()
        mock_ds.form_string = "test"
        mock_ds.template = Template(format=Template.JSON)
        mock_ds.data = None
        mock_ds_get_by_id.return_value = mock_ds
        request = self.factory.get("core_curate_enter_data")
        request._messages = MagicMock()
        request.user = self.user1
        expected_context = {
            "edit": False,
            "form": None,
            "data_structure": mock_ds,
            "page_title": "Enter Data",
        }
        # Act
        EnterDataView.as_view()(request, curate_data_structure_id=1)

        # Assert
        mock_render.assert_called_with(
            request,
            "core_curate_app/user/data-entry/enter_data.html",
            **{
                "assets": {
                    "js": [
                        {
                            "path": "core_main_app/common/js/debounce.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_main_app/common/js/elementViewport.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_curate_app/user/js/enter_data.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_curate_app/user/js/enter_data.raw.js",
                            "is_raw": True,
                        },
                        {
                            "path": "core_parser_app/js/modules.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_parser_app/js/modules.raw.js",
                            "is_raw": True,
                        },
                        {
                            "path": "core_main_app/common/js/XMLTree.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_parser_app/js/autosave.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_parser_app/js/autosave.raw.js",
                            "is_raw": True,
                        },
                        {
                            "path": "core_parser_app/js/buttons.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_curate_app/user/js/buttons.raw.js",
                            "is_raw": True,
                        },
                        {
                            "path": "core_parser_app/js/choice.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_curate_app/user/js/choice.raw.js",
                            "is_raw": True,
                        },
                        {
                            "path": "core_main_app/common/js/data_detail.js",
                            "is_raw": False,
                        },
                        {
                            "path": "https://cdnjs.cloudflare.com/ajax/libs/json-editor/2.14.1/jsoneditor.js",
                            "integrity": "sha512-G93wD4PAiaCg3T4BeJGXNUdwJ4jr6WL0dKUqz0UwZs0jVad7FnJ2r+SlJ50k6+ILkYcQBqt4M5YoFcBWujIH0A==",
                            "is_external": True,
                            "is_raw": False,
                        },
                        {
                            "path": "core_curate_app/user/js/xml_entities_tooltip.js",
                            "is_raw": False,
                        },
                        {
                            "path": "core_curate_app/user/js/xml_entities_tooltip/popover.bs4.js",
                            "is_raw": False,
                        },
                    ],
                    "css": [
                        "core_curate_app/user/css/common.css",
                        "core_curate_app/user/css/xsd_form.css",
                        "core_parser_app/css/use.css",
                        "core_main_app/common/css/modals/download.css",
                        "core_curate_app/user/css/json_form.css",
                    ],
                },
                "context": expected_context,
                "modals": [
                    "core_curate_app/user/data-entry/modals/cancel-changes.html",
                    "core_curate_app/user/data-entry/modals/cancel-form.html",
                    "core_curate_app/user/data-entry/modals/clear-fields.html",
                    "core_main_app/common/modals/download-options.html",
                    "core_curate_app/user/data-entry/modals/save-form.html",
                    "core_curate_app/user/data-entry/modals/use-validation.html",
                    "core_curate_app/user/data-entry/modals/validation-error.html",
                    "core_curate_app/user/data-entry/modals/xml-valid.html",
                    "core_curate_app/user/data-entry/modals/switch_to_text_editor.html",
                ],
            },
        )


class TestViewDataViewInit(TestCase):
    """Unit tests for `ViewDataView.__init__` method."""

    def setUp(self):
        """setUp
        Returns:
        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1")
        self.user1.has_perm = MagicMock()
        self.user1.has_perm.return_value = True

    @override_settings(INSTALLED_APPS=["core_file_preview_app"])
    def test_file_preview_app_installed_adds_correct_js_asset(self):
        """test_file_preview_app_installed_adds_correct_js_asset"""
        result = ViewDataView()

        self.assertIn(
            {
                "path": "core_file_preview_app/user/js/file_preview.js",
                "is_raw": False,
            },
            result.assets["js"],
        )

    @override_settings(INSTALLED_APPS=["core_file_preview_app"])
    def test_file_preview_app_installed_adds_correct_css_asset(self):
        """test_file_preview_app_installed_adds_correct_css_asset"""
        result = ViewDataView()

        self.assertIn(
            "core_file_preview_app/user/css/file_preview.css",
            result.assets["css"],
        )

    @override_settings(INSTALLED_APPS=["core_file_preview_app"])
    def test_file_preview_app_installed_adds_correct_modal_asset(self):
        """test_file_preview_app_installed_adds_correct_modal_asset"""
        result = ViewDataView()

        self.assertIn(
            "core_file_preview_app/user/file_preview_modal.html", result.modals
        )

    @override_settings(INSTALLED_APPS=[])
    def test_file_preview_app_not_installed_adds_no_js_asset(self):
        """test_file_preview_app_not_installed_adds_no_js_asset"""
        result = ViewDataView()

        self.assertNotIn(
            {
                "path": "core_file_preview_app/user/js/file_preview.js",
                "is_raw": False,
            },
            result.assets["js"],
        )

    @override_settings(INSTALLED_APPS=[])
    def test_file_preview_app_not_installed_adds_no_css_asset(self):
        """test_file_preview_app_not_installed_adds_no_css_asset"""
        result = ViewDataView()

        self.assertNotIn(
            "core_file_preview_app/user/css/file_preview.css",
            result.assets["css"],
        )

    @override_settings(INSTALLED_APPS=[])
    def test_file_preview_app_not_installed_adds_no_modal_asset(self):
        """test_file_preview_app_not_installed_adds_no_modal_asset"""
        result = ViewDataView()

        self.assertNotIn(
            "core_file_preview_app/user/file_preview_modal.html", result.modals
        )

    @patch.object(curate_user_views, "render_xml")
    @patch("core_curate_app.views.user.views._get_curate_data_structure_by_id")
    def test_view_data_view_build_context_with_xsd_template_returns_http_200(
        self, mock_ds_get_by_id, mock_render_xml
    ):
        """test_enter_data_view_build_context_with_xsd_template_returns_http_200"""
        # Arrange
        mock_ds = MagicMock()
        mock_ds.form_string = "<root></root>"
        mock_ds.template = Template(format=Template.XSD)
        mock_ds_get_by_id.return_value = mock_ds
        request = self.factory.get("core_curate_view_data")
        request.user = self.user1
        mock_render_xml.return_value = None
        # Act
        response = ViewDataView.as_view()(request, curate_data_structure_id=1)
        # Assert
        self.assertEqual(response.status_code, 200)

    @patch("core_curate_app.views.user.views._get_curate_data_structure_by_id")
    def test_view_data_view_build_context_with_json_template_returns_http_200(
        self, mock_ds_get_by_id
    ):
        """test_view_data_view_build_context_with_json_template_returns_http_200"""
        # Arrange
        mock_ds = MagicMock()
        mock_ds.form_string = "{}"
        mock_ds.template = Template(format=Template.JSON)
        mock_ds_get_by_id.return_value = mock_ds
        request = self.factory.get("core_curate_view_data")
        request.user = self.user1
        # Act
        response = ViewDataView.as_view()(request, curate_data_structure_id=1)
        # Assert
        self.assertEqual(response.status_code, 200)


class TestGenerateRootElementView(TestCase):
    """Unit tests for `generate_root_element` method."""

    def setUp(self):
        """setUp"""
        factory = RequestFactory()
        user1 = create_mock_user(user_id="1", has_perm=True)

        self.request = factory.get("core_curate_cancel_changes")
        self.request.POST = {"id": 1}
        self.request.user = user1

    @patch("core_main_app.components.template.api.get_by_id")
    def test_generate_element_root_raises_xsd_error_if_not_xsd_template(
        self, mock_template_get_by_id
    ):
        """test_generate_element_root_raises_xsd_error_if_not_xsd_template"""
        mock_template = _get_json_template()
        mock_curate_data_structure = MagicMock(template=mock_template)
        mock_template_get_by_id.return_value = mock_template

        with self.assertRaises(XSDError):
            generate_root_element(self.request, mock_curate_data_structure, "")
        self.assertTrue(mock_template_get_by_id.called)


class TestDownloadCurrentDocumentView(TestCase):
    """Test Download Current Document View"""

    def setUp(self):
        """setUp"""
        factory = RequestFactory()
        user1 = create_mock_user(user_id="1", has_perm=True)

        self.request = factory.get("core_curate_download_document")
        self.request.user = user1

    @patch.object(curate_user_views, "render_xml")
    @patch.object(curate_user_views, "curate_data_structure_api")
    def test_download_xml_document_returns_file_without_formatting(
        self,
        mock_curate_data_structure_api,
        mock_render_xml,
    ):
        """test_download_xml_document_returns_file_without_formatting"""
        mock_data = MagicMock(
            template=Template(format=Template.XSD), data=None, user="1"
        )
        mock_curate_data_structure_api.get_by_id.return_value = mock_data

        mock_render_xml.return_value = "<root></root>"

        response = curate_user_views.download_current_document(self.request, 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"<root></root>")

    @patch.object(curate_user_views, "render_xml")
    @patch.object(curate_user_views, "curate_data_structure_api")
    def test_download_xml_document_returns_file_with_formatting_option(
        self,
        mock_curate_data_structure_api,
        mock_render_xml,
    ):
        """test_download_xml_document_returns_file_with_formatting_option"""
        mock_data = MagicMock(
            template=Template(format=Template.XSD), data=None, user="1"
        )
        mock_curate_data_structure_api.get_by_id.return_value = mock_data

        mock_render_xml.return_value = "<root></root>"

        self.request.GET = {"pretty_print": True}
        response = curate_user_views.download_current_document(self.request, 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"<root/>\n")

    @patch.object(curate_user_views, "curate_data_structure_api")
    def test_download_json_document_returns_file_without_formatting(
        self,
        mock_curate_data_structure_api,
    ):
        """test_download_xml_document_returns_file"""
        mock_data = MagicMock(
            template=Template(format=Template.JSON),
            data=None,
            user="1",
            form_string="",
        )
        mock_curate_data_structure_api.get_by_id.return_value = mock_data

        response = curate_user_views.download_current_document(self.request, 1)

        self.assertEqual(response.status_code, 200)

    @patch.object(curate_user_views, "curate_data_structure_api")
    def test_download_json_document_returns_formatted_file(
        self,
        mock_curate_data_structure_api,
    ):
        """test_download_xml_document_returns_file"""
        mock_data = MagicMock(
            template=Template(format=Template.JSON),
            data=None,
            user="1",
            form_string="{}",
        )
        mock_curate_data_structure_api.get_by_id.return_value = mock_data

        self.request.GET = {"pretty_print": True}
        response = curate_user_views.download_current_document(self.request, 1)

        self.assertEqual(response.status_code, 200)


class TestDownloadTemplateView(TestCase):
    """Test Download Template View"""

    def setUp(self):
        """setUp"""
        factory = RequestFactory()
        user1 = create_mock_user(user_id="1", has_perm=True)

        self.request = factory.get("core_curate_download_template")
        self.request.user = user1

    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_views, "curate_data_structure_api")
    def test_download_xsd_template_returns_file_without_formatting(
        self,
        mock_curate_data_structure_api,
        mock_template_get_by_id,
    ):
        """test_download_xsd_template_returns_file_without_formatting"""

        content = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            "</xs:schema>"
        )

        mock_template = Template(format=Template.XSD, content=content)
        mock_data = MagicMock(template=mock_template, data=None, user="1")

        mock_curate_data_structure_api.get_by_id.return_value = mock_data

        mock_template_get_by_id.return_value = mock_template

        response = curate_user_views.download_template(self.request, 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content.decode("utf-8"), content)

    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_views, "curate_data_structure_api")
    def test_download_xsd_template_returns_formatted_file(
        self,
        mock_curate_data_structure_api,
        mock_template_get_by_id,
    ):
        """test_download_xsd_template_returns_formatted_file"""
        content = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">'
            "</xs:schema>"
        )

        mock_template = Template(format=Template.XSD, content=content)
        mock_data = MagicMock(template=mock_template, data=None, user="1")

        mock_curate_data_structure_api.get_by_id.return_value = mock_data

        mock_template_get_by_id.return_value = mock_template

        self.request.GET = {"pretty_print": True}
        response = curate_user_views.download_template(self.request, 1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.content.decode("utf-8"), format_content_xml(content)
        )

    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_views, "curate_data_structure_api")
    def test_download_json_template_returns_file_without_formatting(
        self, mock_curate_data_structure_api, mock_template_get_by_id
    ):
        """test_download_json_template_returns_file_without_formatting"""
        mock_template = Template(format=Template.JSON, content="{}")
        mock_data = MagicMock(template=mock_template, data=None, user="1")
        mock_curate_data_structure_api.get_by_id.return_value = mock_data
        mock_template_get_by_id.return_value = mock_template

        response = curate_user_views.download_template(self.request, 1)

        self.assertEqual(response.status_code, 200)

    @patch("core_main_app.components.template.api.get_by_id")
    @patch.object(curate_user_views, "curate_data_structure_api")
    def test_download_json_document_returns_formatted_file(
        self,
        mock_curate_data_structure_api,
        mock_template_get_by_id,
    ):
        """test_download_json_document_returns_formatted_file"""
        mock_template = Template(format=Template.JSON, content="{}")
        mock_data = MagicMock(template=mock_template, data=None, user="1")
        mock_curate_data_structure_api.get_by_id.return_value = mock_data
        mock_template_get_by_id.return_value = mock_template

        self.request.GET = {"pretty_print": True}
        response = curate_user_views.download_template(self.request, 1)

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
