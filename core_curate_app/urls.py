""" Url router for the curate application
"""
from django.conf.urls import include
from django.urls import re_path

import core_curate_app.views.user.ajax as user_ajax
import core_curate_app.views.user.views as user_views
from core_curate_app.permissions import rights
from core_curate_app.views.common import views as common_views
from core_main_app.utils.decorators import permission_required

urlpatterns = [
    re_path(r"^$", user_views.index, name="core_curate_index"),
    re_path(
        r"^start_curate$", user_ajax.start_curate, name="core_curate_start"
    ),
    re_path(
        r"^enter-data/(?P<curate_data_structure_id>\w+)$",
        user_views.EnterDataView.as_view(),
        name="core_curate_enter_data",
    ),
    # FIXME: url to allow reopening a form with unsaved changes
    #  (may be temporary until curate workflow redesign)
    re_path(
        r"^enter-data/(?P<curate_data_structure_id>\w+)/(?P<reload_unsaved_changes>\w+)$",
        user_views.EnterDataView.as_view(),
        name="core_curate_enter_data",
    ),
    re_path(
        r"^view-data/(?P<curate_data_structure_id>\w+)$",
        user_views.ViewDataView.as_view(),
        name="core_curate_view_data",
    ),
    re_path(
        r"^download-document/(?P<curate_data_structure_id>\w+)$",
        user_views.download_current_document,
        name="core_curate_download_document",
    ),
    re_path(
        r"^download-template/(?P<curate_data_structure_id>\w+)$",
        user_views.download_template,
        name="core_curate_download_template",
    ),
    re_path(
        r"^generate-choice/(?P<curate_data_structure_id>\w+)$",
        user_ajax.generate_choice,
        name="core_curate_generate_choice",
    ),
    re_path(
        r"^generate-element/(?P<curate_data_structure_id>\w+)$",
        user_ajax.generate_element,
        name="core_curate_generate_element",
    ),
    re_path(
        r"^remove-element$",
        user_ajax.remove_element,
        name="core_curate_remove_element",
    ),
    re_path(
        r"^clear-fields$",
        user_ajax.clear_fields,
        name="core_curate_clear_fields",
    ),
    re_path(
        r"^cancel-changes$",
        user_ajax.cancel_changes,
        name="core_curate_cancel_changes",
    ),
    re_path(
        r"^cancel-form$", user_ajax.cancel_form, name="core_curate_cancel_form"
    ),
    re_path(
        r"^xml-editor/form",
        permission_required(
            content_type=rights.CURATE_CONTENT_TYPE,
            permission=rights.CURATE_DATA_STRUCTURE_ACCESS,
        )(common_views.DataStructureXMLEditor.as_view()),
        name="core_curate_app_xml_text_editor_view",
    ),
    re_path(
        r"^json-editor/form",
        permission_required(
            content_type=rights.CURATE_CONTENT_TYPE,
            permission=rights.CURATE_DATA_STRUCTURE_ACCESS,
        )(common_views.DataStructureJSONEditor.as_view()),
        name="core_curate_app_json_text_editor_view",
    ),
    re_path(r"^save-form$", user_ajax.save_form, name="core_curate_save_form"),
    re_path(r"^save-data$", user_ajax.save_data, name="core_curate_save_data"),
    re_path(
        r"^validate-form$",
        user_ajax.validate_form,
        name="core_curate_validate_form",
    ),
    re_path(
        r"^view-form/(?P<curate_data_structure_id>\w+)$",
        permission_required(
            content_type=rights.CURATE_CONTENT_TYPE,
            permission=rights.CURATE_ACCESS,
        )(common_views.FormView.as_view()),
        name="core_curate_view_form",
    ),
    re_path(r"^rest/", include("core_curate_app.rest.urls")),
]
