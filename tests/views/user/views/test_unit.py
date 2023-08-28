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
from core_main_app.commons.exceptions import XSDError
from core_main_app.components.template.models import Template
from core_main_app.utils.tests_tools.MockUser import create_mock_user
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


class TestViewDataViewInit(TestCase):
    """Unit tests for `ViewDataView.__init__` method."""

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


def _get_json_template():
    """Get JSON template

    Returns:

    """
    template = Template()
    template.format = Template.JSON
    template.id_field = 1
    template.content = "{}"
    return template
