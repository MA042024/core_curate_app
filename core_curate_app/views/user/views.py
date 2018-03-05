"""Curate app user views
"""
from core_parser_app.components.data_structure_element import api as data_structure_element_api
from core_parser_app.tools.parser import parser
from core_parser_app.tools.parser.renderer.list import ListRenderer
from core_parser_app.tools.parser.renderer.xml import XmlRenderer
from django.core.urlresolvers import reverse_lazy

import core_curate_app.permissions.rights as rights
import core_main_app.components.template_version_manager.api as template_api
import core_main_app.utils.decorators as decorators
from core_curate_app.components.curate_data_structure import api as curate_data_structure_api
from core_curate_app.utils.parser import get_parser
from core_main_app.commons.exceptions import CoreError, LockError
from core_main_app.components.lock import api as lock_api
from core_main_app.utils.file import get_file_http_response
from core_main_app.utils.rendering import render

# TODO: Add a view for the registry. Ajax code need to be refactored


@decorators.permission_required(content_type=rights.curate_content_type,
                                permission=rights.curate_access, login_url=reverse_lazy("core_main_app_login"))
def index(request):
    """ Page that allows to select a template to start curating.

    Args:
        request:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": 'core_curate_app/user/js/select_template.js',
                "is_raw": False
            },
            {
                "path": 'core_curate_app/user/js/select_template.raw.js',
                "is_raw": True
            },
        ],
        "css": ['core_curate_app/user/css/style.css']
    }

    global_active_template_list = template_api.get_active_global_version_manager()
    user_active_template_list = template_api.get_active_version_manager_by_user_id(request.user.id)

    context = {
        'templates_version_manager': global_active_template_list,
        'userTemplates': user_active_template_list,
    }

    return render(request,
                  'core_curate_app/user/curate.html',
                  # modals=modals,
                  assets=assets,
                  context=context)


# FIXME: allow reopening a form with unsaved changes (may be temporary until curate workflow redesign)
@decorators.permission_required(content_type=rights.curate_content_type,
                                permission=rights.curate_access, login_url=reverse_lazy("core_main_app_login"))
def enter_data(request, curate_data_structure_id, reload_unsaved_changes=False):
    """Load view to enter data.

    Args:
        request:
        curate_data_structure_id:
        reload_unsaved_changes:

    Returns:

    """
    try:
        # get data structure
        curate_data_structure = curate_data_structure_api.get_by_id(curate_data_structure_id)

        # lock from database
        if curate_data_structure.data is not None:
            lock_api.set_lock_object(curate_data_structure.data, request.user)

        # check ownership
        _check_owner(request, accessed_object=curate_data_structure)

        # get xsd string from the template
        xsd_string = curate_data_structure.template.content

        if reload_unsaved_changes:
            # get root element from the data structure
            root_element = curate_data_structure.data_structure_element_root
        else:
            # if form string provided, use it to generate the form
            xml_string = curate_data_structure.form_string

            # get the root element
            root_element = generate_form(xsd_string, xml_string)

            # save the root element in the data structure
            update_data_structure_root(curate_data_structure, root_element)

        # renders the form
        xsd_form = render_form(request, root_element)

        # Set the assets
        assets = {
            "js": [
                {
                    "path": "core_curate_app/user/js/enter_data.js",
                    "is_raw": False
                },
                {
                    "path": "core_curate_app/user/js/enter_data.raw.js",
                    "is_raw": True
                },
                {
                    "path": "core_parser_app/js/modules.js",
                    "is_raw": False
                },
                {
                    "path": "core_parser_app/js/modules.raw.js",
                    "is_raw": True
                },
                {
                    "path": 'core_main_app/common/js/XMLTree.js',
                    "is_raw": False
                },
                {
                    "path": "core_parser_app/js/autosave.js",
                    "is_raw": False
                },
                {
                    "path": "core_parser_app/js/autosave.raw.js",
                    "is_raw": True
                },
                {
                    "path": "core_parser_app/js/buttons.js",
                    "is_raw": False
                },
                {
                    "path": "core_curate_app/user/js/buttons.raw.js",
                    "is_raw": True
                },
                {
                    "path": "core_parser_app/js/choice.js",
                    "is_raw": False
                },
                {
                    "path": "core_curate_app/user/js/choice.raw.js",
                    "is_raw": True
                },
            ],
            "css": ['core_curate_app/user/css/xsd_form.css',
                    'core_parser_app/css/use.css']
        }

        modals = [
            'core_curate_app/user/data-entry/modals/cancel-changes.html',
            'core_curate_app/user/data-entry/modals/cancel-form.html',
            'core_curate_app/user/data-entry/modals/clear-fields.html',
            'core_curate_app/user/data-entry/modals/download-options.html',
            'core_curate_app/user/data-entry/modals/save-form.html',
            'core_curate_app/user/data-entry/modals/use-validation.html',
            'core_curate_app/user/data-entry/modals/xml-error.html',
            'core_curate_app/user/data-entry/modals/xml-valid.html',
        ]

        # Set the context
        context = {
            "edit": True if curate_data_structure.data is not None else False,
            "xsd_form": xsd_form,
            "data_structure": curate_data_structure,
        }

        return render(request,
                      'core_curate_app/user/data-entry/enter_data.html',
                      assets=assets,
                      context=context,
                      modals=modals)
    except LockError, ler:
        return render(request,
                      'core_curate_app/user/errors.html',
                      assets={},
                      context={'errors': ler.message})
    except Exception, e:
        try:
            # unlock from database
            if curate_data_structure is not None and curate_data_structure.data is not None:
                lock_api.remove_lock_on_object(curate_data_structure.data, request.user)
        except:
            pass

        return render(request,
                      'core_curate_app/user/errors.html',
                      assets={},
                      context={'errors': e.message})


@decorators.permission_required(content_type=rights.curate_content_type,
                                permission=rights.curate_access, login_url=reverse_lazy("core_main_app_login"))
def view_data(request, curate_data_structure_id):
    """Load the view to review data.

    Args:
        request:
        curate_data_structure_id:

    Returns:

    """
    try:
        curate_data_structure = _get_curate_data_structure_by_id(curate_data_structure_id, request)

        # generate xml string
        xml_string = render_xml(curate_data_structure.data_structure_element_root)

        # Set the assets
        assets = {
            "js": [
                {
                    "path": "core_curate_app/user/js/view_data.js",
                    "is_raw": False
                },
                {
                    "path": "core_curate_app/user/js/view_data.raw.js",
                    "is_raw": True
                },
                {
                    "path": "core_main_app/common/js/XMLTree.js",
                    "is_raw": False
                },
            ],
            "css": ['core_main_app/common/css/XMLTree.css']
        }

        # Set the context
        context = {
            "edit": True if curate_data_structure.data is not None else False,
            "xml_string": xml_string,
            "data_structure": curate_data_structure,
        }

        modals = [
            'core_curate_app/user/data-review/modals/save-error.html',
        ]

        return render(request,
                      'core_curate_app/user/data-review/view_data.html',
                      assets=assets,
                      context=context,
                      modals=modals)
    except Exception, e:
        return render(request,
                      'core_curate_app/user/errors.html',
                      assets={},
                      context={'errors': e.message})


@decorators.permission_required(content_type=rights.curate_content_type,
                                permission=rights.curate_access, login_url=reverse_lazy("core_main_app_login"))
def download_current_xml(request, curate_data_structure_id):
    """Make the current XML document available for download.

    Args:
        request:
        curate_data_structure_id:

    Returns:

    """
    # get curate data structure
    curate_data_structure = curate_data_structure_api.get_by_id(curate_data_structure_id)
    # check ownership
    _check_owner(request, accessed_object=curate_data_structure)

    # generate xml string
    xml_data = render_xml(curate_data_structure.data_structure_element_root)

    # build response with file
    return get_file_http_response(file_content=xml_data,
                                  file_name=curate_data_structure.name,
                                  content_type='application/xml',
                                  extension='xml')


@decorators.permission_required(content_type=rights.curate_content_type,
                                permission=rights.curate_access, login_url=reverse_lazy("core_main_app_login"))
def download_xsd(request, curate_data_structure_id):
    """Make the current XSD available for download.

    Args:
        request:
        curate_data_structure_id:

    Returns:

    """
    # get curate data structure
    curate_data_structure = curate_data_structure_api.get_by_id(curate_data_structure_id)
    # check ownership
    _check_owner(request, accessed_object=curate_data_structure)

    # get the template
    template = curate_data_structure.template
    # return the file
    return get_file_http_response(file_content=template.content,
                                  file_name=template.filename,
                                  content_type='application/xsd',
                                  extension='.xsd')


def generate_form(xsd_string, xml_string=None):
    """Generate the form using the parser, returns the root element.

    Args:
        xsd_string:
        xml_string:

    Returns:

    """
    # build parser
    parser = get_parser()
    # generate form
    root_element_id = parser.generate_form(xsd_string, xml_string)
    # get the root element
    root_element = data_structure_element_api.get_by_id(root_element_id)

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


def render_xml(root_element):
    """Render the XML.

    Args:
        root_element:

    Returns:

    """
    # build XML renderer
    xml_renderer = XmlRenderer(root_element)

    # generate xml data
    xml_data = xml_renderer.render()

    return xml_data


def update_data_structure_root(curate_data_structure, root_element):
    """Update the data structure with a root element.

    Args:
        curate_data_structure:
        root_element:

    Returns:

    """
    # FIXME: do the delete branch asynchronously
    # Delete data structure elements
    if curate_data_structure.data_structure_element_root is not None:
        parser.delete_branch_from_db(curate_data_structure.data_structure_element_root.id)
    # set the root element in the data structure
    curate_data_structure.data_structure_element_root = root_element
    # save the data structure
    curate_data_structure_api.upsert(curate_data_structure)


# FIXME: make this check more general
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
            raise CoreError("You are not the owner of the resource that you are trying to access")


def _get_curate_data_structure_by_id(curate_data_structure_id, request):
    """ Get the curate data structure by its id.

    Args: curate_data_structure_id:
          request:
    Returns:
    """

    # get data structure
    curate_data_structure = curate_data_structure_api.get_by_id(curate_data_structure_id)
    # check ownership
    _check_owner(request, accessed_object=curate_data_structure)

    return curate_data_structure
