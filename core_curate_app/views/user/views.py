"""Curate app user views
"""
import json
import logging
from builtins import any
from typing import Dict, List

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.conf import settings

import core_main_app.components.template.api as template_api
import core_main_app.components.template_version_manager.api as template_version_manager_api
from core_curate_app.components.curate_data_structure import (
    api as curate_data_structure_api,
)
from core_curate_app.permissions import rights
from core_curate_app.utils.parser import get_parser
from core_main_app.access_control.api import check_can_write
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.constants import (
    DATA_FILE_CONTENT_TYPE_FOR_TEMPLATE_FORMAT,
    DATA_FILE_EXTENSION_FOR_TEMPLATE_FORMAT,
    TEMPLATE_FILE_EXTENSION_FOR_TEMPLATE_FORMAT,
    TEMPLATE_FILE_CONTENT_TYPE_FOR_TEMPLATE_FORMAT,
)
from core_main_app.commons.exceptions import (
    LockError,
    ModelError,
    DoesNotExist,
    XSDError,
)
from core_main_app.components.lock import api as lock_api
from core_main_app.components.template.models import Template
from core_main_app.utils import decorators
from core_main_app.utils.boolean import to_bool
from core_main_app.utils.file import get_file_http_response
from core_main_app.utils.labels import get_form_label
from core_main_app.utils.rendering import render
from core_main_app.utils.xml import format_content_xml
from core_parser_app.components.data_structure_element import (
    api as data_structure_element_api,
)
from core_parser_app.tools.parser.exceptions import ParserError
from core_parser_app.tools.parser.renderer.list import ListRenderer
from core_parser_app.tools.parser.renderer.xml import XmlRenderer

logger = logging.getLogger(__name__)

# TODO: Add a view for the registry. Ajax code need to be refactored


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
)
def index(request):
    """Page that allows to select a template to start curating.

    Args:
        request:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": "core_curate_app/user/js/select_template.js",
                "is_raw": False,
            },
            {
                "path": "core_main_app/common/js/tooltip.js",
                "is_raw": False,
            },
            {
                "path": "core_curate_app/user/js/select_template.raw.js",
                "is_raw": True,
            },
        ],
        "css": [
            "core_curate_app/user/css/common.css",
            "core_curate_app/user/css/style.css",
        ],
    }

    global_active_template_list = (
        template_version_manager_api.get_active_global_version_manager(
            request=request
        )
    )
    user_active_template_list = (
        template_version_manager_api.get_active_version_manager_by_user_id(
            request=request
        )
    )

    context = {
        "templates_version_manager": global_active_template_list,
        "userTemplates": user_active_template_list,
    }

    # Set page title
    context.update({"page_title": "Curate"})

    return render(
        request,
        "core_curate_app/user/curate.html",
        assets=assets,
        context=context,
    )


# FIXME: allow reopening a form with unsaved changes (may be temporary until
#  curate workflow redesign)
class EnterDataView(View):
    """Page that allows to enter a data view."""

    def __init__(self):
        super().__init__()
        self.assets = {
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
                {"path": "core_parser_app/js/modules.js", "is_raw": False},
                {"path": "core_parser_app/js/modules.raw.js", "is_raw": True},
                {
                    "path": "core_main_app/common/js/XMLTree.js",
                    "is_raw": False,
                },
                {"path": "core_parser_app/js/autosave.js", "is_raw": False},
                {"path": "core_parser_app/js/autosave.raw.js", "is_raw": True},
                {"path": "core_parser_app/js/buttons.js", "is_raw": False},
                {
                    "path": "core_curate_app/user/js/buttons.raw.js",
                    "is_raw": True,
                },
                {"path": "core_parser_app/js/choice.js", "is_raw": False},
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
            ],
            "css": [
                "core_curate_app/user/css/common.css",
                "core_curate_app/user/css/xsd_form.css",
                "core_parser_app/css/use.css",
                "core_main_app/common/css/modals/download.css",
            ],
        }

        if settings.ENABLE_XML_ENTITIES_TOOLTIPS:
            self.assets["js"].append(
                {
                    "path": "core_curate_app/user/js/xml_entities_tooltip.js",
                    "is_raw": False,
                }
            )
            if settings.BOOTSTRAP_VERSION.startswith("4"):
                self.assets["js"].append(
                    {
                        "path": "core_curate_app/user/js/xml_entities_tooltip/popover.bs4.js",
                        "is_raw": False,
                    }
                )
            elif settings.BOOTSTRAP_VERSION.startswith("5"):
                self.assets["js"].append(
                    {
                        "path": "core_curate_app/user/js/xml_entities_tooltip/popover.bs5.js",
                        "is_raw": False,
                    }
                )

        self.modals = [
            "core_curate_app/user/data-entry/modals/cancel-changes.html",
            "core_curate_app/user/data-entry/modals/cancel-form.html",
            "core_curate_app/user/data-entry/modals/clear-fields.html",
            "core_main_app/common/modals/download-options.html",
            "core_curate_app/user/data-entry/modals/save-form.html",
            "core_curate_app/user/data-entry/modals/use-validation.html",
            "core_curate_app/user/data-entry/modals/validation-error.html",
            "core_curate_app/user/data-entry/modals/xml-valid.html",
            "core_curate_app/user/data-entry/modals/switch_to_text_editor.html",
        ]

    def build_context(
        self, request, curate_data_structure, reload_unsaved_changes
    ):
        """Build the context of the view

        Args:
            request:
            curate_data_structure:
            reload_unsaved_changes:

        Returns:

        """
        if curate_data_structure.template.format == Template.XSD:
            if reload_unsaved_changes:
                # get root element from the data structure
                root_element = (
                    curate_data_structure.data_structure_element_root
                )
            else:
                # if form string provided, use it to generate the form
                xml_string = curate_data_structure.form_string

                root_element = generate_root_element(
                    request, curate_data_structure, xml_string
                )

            # renders the form
            form = render_form(request, root_element)

        else:
            form = None

        return {
            "edit": True if curate_data_structure.data is not None else False,
            "form": form,
            "data_structure": curate_data_structure,
        }

    @method_decorator(
        decorators.permission_required(
            content_type=rights.CURATE_CONTENT_TYPE,
            permission=rights.CURATE_ACCESS,
        )
    )
    def get(
        self, request, curate_data_structure_id, reload_unsaved_changes=False
    ):
        """Load view to enter data.

        Args:
            request:
            curate_data_structure_id:
            reload_unsaved_changes:

        Returns:

        """
        curate_data_structure = None
        try:
            # Retrieve CurateDataStructure and lock the object for the current
            # user.
            curate_data_structure = _get_curate_data_structure_by_id(
                curate_data_structure_id, request
            )

            # Lock from database
            if curate_data_structure.data is not None:
                lock_api.set_lock_object(
                    curate_data_structure.data, request.user
                )

            # Build context
            context = self.build_context(
                request, curate_data_structure, reload_unsaved_changes
            )

            # additional style for the JSON form
            if curate_data_structure.template.format == Template.JSON:
                self.assets["css"].append(
                    "core_curate_app/user/css/json_form.css"
                )

            # Set page title
            context.update({"page_title": "Enter Data"})

            return render(
                request,
                "core_curate_app/user/data-entry/enter_data.html",
                assets=self.assets,
                context=context,
                modals=self.modals,
            )
        except (LockError, AccessControlError, ModelError, DoesNotExist) as ex:
            return render(
                request,
                "core_curate_app/user/errors.html",
                assets={},
                context={"errors": str(ex), "page_title": "Error"},
            )
        except ParserError as parser_exception:
            messages.add_message(
                self.request,
                messages.ERROR,
                str(parser_exception),
            )
            url = (
                reverse("core_curate_app_xml_text_editor_view")
                + f"?id={str(curate_data_structure_id)}"
            )
            return HttpResponseRedirect(url)
        except Exception as exception:
            try:
                # Unlock from database
                if (
                    curate_data_structure is not None
                    and curate_data_structure.data is not None
                ):
                    lock_api.remove_lock_on_object(
                        curate_data_structure.data, request.user
                    )
            except Exception as lock_exc:
                # CurateDataStructure not found, continue search
                logger.warning(
                    "'EnterDataView.get' threw an exception:%s", str(lock_exc)
                )

            return render(
                request,
                "core_curate_app/user/errors.html",
                assets={},
                context={"errors": str(exception), "page_title": "Error"},
            )


class ViewDataView(View):
    """
    Page that allows to view a data.

    Args:
        View:

    Returns:

    """

    def __init__(self):
        super().__init__()
        self.assets: Dict[str, List[any]] = {
            "js": [
                {
                    "path": "core_curate_app/user/js/view_data.js",
                    "is_raw": False,
                },
                {
                    "path": "core_curate_app/user/js/view_data.raw.js",
                    "is_raw": True,
                },
                {
                    "path": "core_main_app/common/js/XMLTree.js",
                    "is_raw": False,
                },
                {
                    "path": "core_main_app/common/js/data_detail.js",
                    "is_raw": False,
                },
            ],
            "css": [
                "core_main_app/common/css/XMLTree.css",
                "core_main_app/common/css/modals/download.css",
            ],
        }

        self.modals = [
            "core_curate_app/user/data-review/modals/save-error.html",
            "core_main_app/common/modals/download-options.html",
        ]

        if "core_file_preview_app" in settings.INSTALLED_APPS:
            self.assets["js"].extend(
                [
                    {
                        "path": "core_file_preview_app/user/js/file_preview.js",
                        "is_raw": False,
                    }
                ]
            )
            self.assets["css"].append(
                "core_file_preview_app/user/css/file_preview.css"
            )
            self.modals.append(
                "core_file_preview_app/user/file_preview_modal.html"
            )

    def build_context(self, request, curate_data_structure):
        """Build form string from CurateDataStructure

        Args:
            request:
            curate_data_structure:

        Returns:
        """
        if curate_data_structure.template.format == Template.XSD:
            content = render_xml(
                request, curate_data_structure.data_structure_element_root
            )
        else:
            content = curate_data_structure.form_string

        return {
            "edit": True if curate_data_structure.data is not None else False,
            "form_string": content,
            "data_structure": curate_data_structure,
        }

    @method_decorator(
        decorators.permission_required(
            content_type=rights.CURATE_CONTENT_TYPE,
            permission=rights.CURATE_ACCESS,
        )
    )
    def get(self, request, curate_data_structure_id):
        """Get data view

        Args:
            request:
            curate_data_structure_id:

        Returns:
        """

        try:
            curate_data_structure = _get_curate_data_structure_by_id(
                curate_data_structure_id, request
            )

            # Build Context
            context = self.build_context(request, curate_data_structure)
            # Set page title
            context.update({"page_title": "View Data"})

            return render(
                request,
                "core_curate_app/user/data-review/view_data.html",
                assets=self.assets,
                context=context,
                modals=self.modals,
            )
        except Exception as exception:
            return render(
                request,
                "core_curate_app/user/errors.html",
                assets={},
                context={"errors": str(exception), "page_title": "Error"},
            )


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
)
def download_current_document(request, curate_data_structure_id):
    """Make the current document available for download.

    Args:
        request:
        curate_data_structure_id:

    Returns:

    """
    # get curate data structure
    curate_data_structure = _get_curate_data_structure_by_id(
        curate_data_structure_id, request
    )
    # get pretty print bool
    prettify = request.GET.get("pretty_print", False)

    if curate_data_structure.template.format == Template.XSD:
        # generate xml string
        content = render_xml(
            request, curate_data_structure.data_structure_element_root
        )
        # prettify content
        if to_bool(prettify):
            content = format_content_xml(content)

    else:
        content = curate_data_structure.form_string
        # prettify content
        if to_bool(prettify):
            content = json.dumps(json.loads(content), indent=2)

    # build response with file
    return get_file_http_response(
        file_content=content,
        file_name=curate_data_structure.name,
        content_type=DATA_FILE_CONTENT_TYPE_FOR_TEMPLATE_FORMAT[
            curate_data_structure.template.format
        ],
        extension=DATA_FILE_EXTENSION_FOR_TEMPLATE_FORMAT[
            curate_data_structure.template.format
        ],
    )


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
)
def download_template(request, curate_data_structure_id):
    """Make the current template available for download.

    Args:
        request:
        curate_data_structure_id:

    Returns:

    """
    # get curate data structure
    curate_data_structure = _get_curate_data_structure_by_id(
        curate_data_structure_id, request
    )

    # get the template
    template = template_api.get_by_id(
        str(curate_data_structure.template.id), request=request
    )
    # get pretty print bool
    prettify = request.GET.get("pretty_print", False)

    # get the template content
    content = template.content
    if template.format == Template.XSD:
        # prettify content
        if to_bool(prettify):
            content = format_content_xml(content)
    else:
        if to_bool(prettify):
            content = json.dumps(json.loads(content), indent=2)

    # return the file
    return get_file_http_response(
        file_content=content,
        file_name=template.filename,
        content_type=TEMPLATE_FILE_CONTENT_TYPE_FOR_TEMPLATE_FORMAT[
            template.format
        ],
        extension=TEMPLATE_FILE_EXTENSION_FOR_TEMPLATE_FORMAT[template.format],
    )


def generate_form(
    xsd_string, xml_string=None, data_structure=None, request=None
):
    """Generate the form using the parser, returns the root element.

    Args:
        xsd_string:
        xml_string:
        data_structure:
        request:

    Returns:

    """
    # build parser
    parser = get_parser(request=request)
    # generate form
    root_element_id = parser.generate_form(
        xsd_string, xml_string, data_structure, request=request
    )
    # get the root element
    root_element = data_structure_element_api.get_by_id(
        root_element_id, request
    )

    return root_element


def render_form(request, root_element):
    """Render the form.

    Args:
        request:
        root_element:

    Returns:

    """
    # build a renderer
    renderer = ListRenderer(root_element, request)
    # render the form
    xsd_form = renderer.render()

    return xsd_form


def generate_root_element(request, curate_data_structure, xml_string):
    """Render the updated form.

    Args:
        request:
        curate_data_structure:
        xml_string:

    Returns:

    """
    # get xsd string from the template
    template = template_api.get_by_id(
        str(curate_data_structure.template.id), request=request
    )
    # check template format
    if template.format != Template.XSD:
        raise XSDError("Template format not supported.")

    # get the root element
    root_element = generate_form(
        template.content,
        xml_string,
        data_structure=curate_data_structure,
        request=request,
    )

    # save the root element in the data structure
    curate_data_structure_api.update_data_structure_root(
        curate_data_structure, root_element, request.user
    )

    return root_element


def render_xml(request, root_element):
    """Render the XML.

    Args:
        request:
        root_element:

    Returns:

    """
    # build XML renderer
    xml_renderer = XmlRenderer(root_element, request)

    # generate xml data
    xml_data = xml_renderer.render()

    return xml_data


def _get_curate_data_structure_by_id(curate_data_structure_id, request):
    """Get the curate data structure by its id.

    Args: curate_data_structure_id:
          request:
    Returns:
    """

    # get data structure
    curate_data_structure = curate_data_structure_api.get_by_id(
        curate_data_structure_id, request.user
    )

    # If not link to a data, only ownership check
    if curate_data_structure.data is None:
        # check ownership
        _check_owner(request, accessed_object=curate_data_structure)
    # Check based on the data
    else:
        # check can write data
        _check_can_write_data(request, accessed_object=curate_data_structure)

    return curate_data_structure


def _check_owner(request, accessed_object):
    """Check if the object can be accessed by the user.

    Args:
        request:
        accessed_object:

    Returns:

    """
    # Super user can access everything
    if not request.user.is_superuser:
        # If not the owner of the accessed object
        if str(request.user.id) != accessed_object.user:
            raise AccessControlError(
                "You are not the owner of the "
                + get_form_label()
                + " that you are trying to access"
            )


def _check_can_write_data(request, accessed_object):
    """Check if the object can be accessed by the user in write mode.

    Args:
        request:
        accessed_object:

    Returns:

    """
    try:
        # Super user can access everything
        if not request.user.is_superuser:
            check_can_write(accessed_object.data, request.user)
    except AccessControlError as ace:
        raise ace
