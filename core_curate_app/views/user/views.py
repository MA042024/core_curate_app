"""Curate app user views
"""
import logging
from builtins import any
from typing import Dict, List

from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

import core_main_app.components.template_version_manager.api as template_version_manager_api
import core_main_app.components.template.api as template_api
from core_main_app.components.lock import api as lock_api
from core_main_app.utils import decorators
from core_main_app.commons.exceptions import LockError, ModelError, DoesNotExist
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.access_control.api import check_can_write

from core_main_app.utils.file import get_file_http_response
from core_main_app.utils.labels import get_form_label
from core_main_app.utils.rendering import render
from core_main_app.utils.boolean import to_bool
from core_main_app.utils.xml import format_content_xml
from core_parser_app.components.data_structure_element import (
    api as data_structure_element_api,
)
from core_parser_app.tools.parser.renderer.list import ListRenderer
from core_parser_app.tools.parser.renderer.xml import XmlRenderer

from core_curate_app.components.curate_data_structure import (
    api as curate_data_structure_api,
)
from core_curate_app.permissions import rights
from core_curate_app.settings import INSTALLED_APPS, ENABLE_XML_ENTITIES_TOOLTIPS
from core_curate_app.utils.parser import get_parser

logger = logging.getLogger(__name__)

# TODO: Add a view for the registry. Ajax code need to be refactored


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
    login_url=reverse_lazy("core_main_app_login"),
)
def index(request):
    """Page that allows to select a template to start curating.

    Args:
        request:

    Returns:

    """
    assets = {
        "js": [
            {"path": "core_curate_app/user/js/select_template.js", "is_raw": False},
            {"path": "core_curate_app/user/js/select_template.raw.js", "is_raw": True},
        ],
        "css": [
            "core_curate_app/user/css/common.css",
            "core_curate_app/user/css/style.css",
        ],
    }

    global_active_template_list = (
        template_version_manager_api.get_active_global_version_manager(request=request)
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

    return render(
        request,
        "core_curate_app/user/curate.html",
        # modals=modals,
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
                {"path": "core_main_app/common/js/debounce.js", "is_raw": False},
                {"path": "core_main_app/common/js/elementViewport.js", "is_raw": False},
                {"path": "core_curate_app/user/js/enter_data.js", "is_raw": False},
                {"path": "core_curate_app/user/js/enter_data.raw.js", "is_raw": True},
                {"path": "core_parser_app/js/modules.js", "is_raw": False},
                {"path": "core_parser_app/js/modules.raw.js", "is_raw": True},
                {"path": "core_main_app/common/js/XMLTree.js", "is_raw": False},
                {"path": "core_parser_app/js/autosave.js", "is_raw": False},
                {"path": "core_parser_app/js/autosave.raw.js", "is_raw": True},
                {"path": "core_parser_app/js/buttons.js", "is_raw": False},
                {"path": "core_curate_app/user/js/buttons.raw.js", "is_raw": True},
                {"path": "core_parser_app/js/choice.js", "is_raw": False},
                {"path": "core_curate_app/user/js/choice.raw.js", "is_raw": True},
                {"path": "core_curate_app/user/js/download.raw.js", "is_raw": True},
                {"path": "core_main_app/common/js/modals/download.js", "is_raw": True},
                {"path": "core_main_app/common/js/data_detail.js", "is_raw": False},
            ],
            "css": [
                "core_curate_app/user/css/common.css",
                "core_curate_app/user/css/xsd_form.css",
                "core_parser_app/css/use.css",
            ],
        }

        if ENABLE_XML_ENTITIES_TOOLTIPS:
            self.assets["js"].append(
                {
                    "path": "core_curate_app/user/js/xml_entities_tooltip.js",
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
            "core_curate_app/user/data-entry/modals/xml-error.html",
            "core_curate_app/user/data-entry/modals/xml-valid.html",
        ]

    def build_context(self, request, curate_data_structure, reload_unsaved_changes):
        """Build the context of the view

        Args:
            request:
            curate_data_structure:
            reload_unsaved_changes:

        Returns:

        """
        if reload_unsaved_changes:
            # get root element from the data structure
            root_element = curate_data_structure.data_structure_element_root
        else:
            # if form string provided, use it to generate the form
            xml_string = curate_data_structure.form_string

            root_element = generate_root_element(
                request, curate_data_structure, xml_string
            )

        # renders the form
        xsd_form = render_form(request, root_element)

        return {
            "edit": True if curate_data_structure.data is not None else False,
            "xsd_form": xsd_form,
            "data_structure": curate_data_structure,
        }

    @method_decorator(
        decorators.permission_required(
            content_type=rights.CURATE_CONTENT_TYPE,
            permission=rights.CURATE_ACCESS,
            login_url=reverse_lazy("core_main_app_login"),
        )
    )
    def get(self, request, curate_data_structure_id, reload_unsaved_changes=False):
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
                lock_api.set_lock_object(curate_data_structure.data, request.user)

            # Check if we need to change the user. Code executed only if the
            # data is unlocked. set_lock_object() raises LockError.
            if str(request.user.id) != curate_data_structure.user:
                curate_data_structure.user = str(request.user.id)
                curate_data_structure = curate_data_structure_api.upsert(
                    curate_data_structure, request.user
                )

            return render(
                request,
                "core_curate_app/user/data-entry/enter_data.html",
                assets=self.assets,
                context=self.build_context(
                    request, curate_data_structure, reload_unsaved_changes
                ),
                modals=self.modals,
            )
        except (LockError, AccessControlError, ModelError, DoesNotExist) as ex:
            return render(
                request,
                "core_curate_app/user/errors.html",
                assets={},
                context={"errors": str(ex)},
            )
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
                context={"errors": str(exception)},
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
                {"path": "core_curate_app/user/js/view_data.js", "is_raw": False},
                {"path": "core_curate_app/user/js/view_data.raw.js", "is_raw": True},
                {"path": "core_main_app/common/js/XMLTree.js", "is_raw": False},
                {"path": "core_curate_app/user/js/download.raw.js", "is_raw": True},
                {"path": "core_main_app/common/js/modals/download.js", "is_raw": True},
                {"path": "core_main_app/common/js/data_detail.js", "is_raw": False},
            ],
            "css": ["core_main_app/common/css/XMLTree.css"],
        }

        self.modals = [
            "core_curate_app/user/data-review/modals/save-error.html",
            "core_main_app/common/modals/download-options.html",
        ]

    def build_context(self, request, curate_data_structure):
        """Build XML string from CurateDataStructure

        Args:
            request:
            curate_data_structure:

        Returns:
        """
        xml_string = render_xml(
            request, curate_data_structure.data_structure_element_root
        )

        return {
            "edit": True if curate_data_structure.data is not None else False,
            "xml_string": xml_string,
            "data_structure": curate_data_structure,
        }

    @method_decorator(
        decorators.permission_required(
            content_type=rights.CURATE_CONTENT_TYPE,
            permission=rights.CURATE_ACCESS,
            login_url=reverse_lazy("core_main_app_login"),
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

            if "core_file_preview_app" in INSTALLED_APPS:
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
                self.modals.append("core_file_preview_app/user/file_preview_modal.html")

            return render(
                request,
                "core_curate_app/user/data-review/view_data.html",
                assets=self.assets,
                context=self.build_context(request, curate_data_structure),
                modals=self.modals,
            )
        except Exception as exception:
            return render(
                request,
                "core_curate_app/user/errors.html",
                assets={},
                context={"errors": str(exception)},
            )


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
    login_url=reverse_lazy("core_main_app_login"),
)
def download_current_xml(request, curate_data_structure_id):
    """Make the current XML document available for download.

    Args:
        request:
        curate_data_structure_id:

    Returns:

    """
    # get curate data structure
    curate_data_structure = _get_curate_data_structure_by_id(
        curate_data_structure_id, request
    )

    # generate xml string
    xml_data = render_xml(request, curate_data_structure.data_structure_element_root)

    # get pretty print bool
    prettify = request.GET.get("pretty_print", False)

    # prettify content
    if to_bool(prettify):
        xml_data = format_content_xml(xml_data)

    # build response with file
    return get_file_http_response(
        file_content=xml_data,
        file_name=curate_data_structure.name,
        content_type="application/xml",
        extension="xml",
    )


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
    login_url=reverse_lazy("core_main_app_login"),
)
def download_xsd(request, curate_data_structure_id):
    """Make the current XSD available for download.

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

    # get the template content
    content = template.content

    # get pretty print bool
    prettify = request.GET.get("pretty_print", False)

    # prettify content
    if to_bool(prettify):
        content = format_content_xml(content)

    # return the file
    return get_file_http_response(
        file_content=content,
        file_name=template.filename,
        content_type="application/xsd",
        extension=".xsd",
    )


def generate_form(xsd_string, xml_string=None, data_structure=None, request=None):
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
    root_element = data_structure_element_api.get_by_id(root_element_id, request)

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
