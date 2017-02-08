"""Curate app user views
"""
from django.http.response import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse_lazy
from django.contrib.staticfiles import finders
from cStringIO import StringIO
from os.path import join

import core_main_app.utils.decorators as decorators
import core_curate_app.permissions.rights as rights

from core_curate_app.utils.parser import get_parser
from core_main_app.commons.exceptions import CoreError
from core_main_app.utils.rendering import render
from core_main_app.utils.xml import xsl_transform
from core_parser_app.components.data_structure import api as data_structure_api
from core_parser_app.components.data_structure_element import api as data_structure_element_api
from core_parser_app.tools.parser.renderer.list import ListRenderer
from core_parser_app.tools.parser.renderer.xml import XmlRenderer
# Do not delete the line below because get_by_id needs it
from core_curate_app.components.curate_data_structure.models import CurateDataStructure
import core_main_app.components.template_version_manager.api as template_api

# TODO: Add a view for the registry. Ajax code need to be refactored


@decorators.permission_required(content_type=rights.curate_content_type,
                                permission=rights.curate_access, login_url=reverse_lazy("core_website_login"))
def index(request):
    """ Page that allows to select a template to start curating

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


@decorators.permission_required(content_type=rights.curate_content_type,
                                permission=rights.curate_access, login_url=reverse_lazy("core_website_login"))
def enter_data(request, curate_data_structure_id):
    """Loads view to enter data

    Args:
        request:
        curate_data_structure_id:

    Returns:

    """
    try:
        # get data structure
        curate_data_structure = data_structure_api.get_by_id(curate_data_structure_id)
        # check ownership
        _check_owner(request, accessed_object=curate_data_structure)

        # curate data structure is not generated
        if curate_data_structure.data_structure_element_root is None:
            # get xsd string from the template
            xsd_string = curate_data_structure.template.content

            # if form string provided, use it to generate the form
            if curate_data_structure.form_string is not None:
                # a form is being edited
                xml_string = curate_data_structure.form_string
            else:
                xml_string = None

            # get the root element
            root_element = generate_form(request, xsd_string, xml_string)

            # save the root element in the data structure
            update_data_structure_root(curate_data_structure, root_element)

            # renders the form
            xsd_form = render_form(request, root_element)
        else:
            # renders the form
            xsd_form = render_form(request, curate_data_structure.data_structure_element_root)

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
                    "path": "core_curate_app/user/js/modules.js",
                    "is_raw": False
                },
                {
                    "path": "core_curate_app/user/js/modules.raw.js",
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
            "css": ['core_curate_app/user/css/xsd_form.css']
        }

        # Set the context
        context = {
            "edit": True if curate_data_structure.data is not None else False,
            "xsd_form": xsd_form,
            "data_structure": curate_data_structure,
        }

        return render(request,
                      'core_curate_app/user/enter_data.html',
                      assets=assets,
                      context=context)
    except Exception, e:
        return render(request,
                      'core_curate_app/user/errors.html',
                      assets={},
                      context={'errors': e.message})


@decorators.permission_required(content_type=rights.curate_content_type,
                                permission=rights.curate_access, login_url=reverse_lazy("core_website_login"))
def view_data(request, curate_data_structure_id):
    """Load the view to review data

    Args:
        request:
        curate_data_structure_id:

    Returns:

    """
    try:
        # get data structure
        curate_data_structure = data_structure_api.get_by_id(curate_data_structure_id)
        # check ownership
        _check_owner(request, accessed_object=curate_data_structure)

        # generate xml string
        xml_string = render_xml(curate_data_structure.data_structure_element_root)

        # loads XSLT
        xslt_path = finders.find(join('core_main_app', 'common', 'xsl', 'xml2html.xsl'))
        # reads XSLT
        xslt_string = _read_file_content(xslt_path)
        # transform XML to HTML
        xml_to_html_string = xsl_transform(xml_string, xslt_string)

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
            "xml_tree": xml_to_html_string,
            "data_structure": curate_data_structure,
        }

        return render(request,
                      'core_curate_app/user/view_data.html',
                      assets=assets,
                      context=context)
    except Exception, e:
        return render(request,
                      'core_curate_app/user/errors.html',
                      assets={},
                      context={'errors': e.message})


@decorators.permission_required(content_type=rights.curate_content_type,
                                permission=rights.curate_access, login_url=reverse_lazy("core_website_login"))
def download_current_xml(request, curate_data_structure_id):
    """Makes the current XML document available for download.

    Args:
        request:
        curate_data_structure_id:

    Returns:

    """
    # get curate data structure
    curate_data_structure = data_structure_api.get_by_id(curate_data_structure_id)
    # check ownership
    _check_owner(request, accessed_object=curate_data_structure)

    # generate xml string
    xml_data = render_xml(curate_data_structure.data_structure_element_root)
    # build a file
    # TODO: test encoding
    xml_data_file = StringIO(xml_data.encode('utf-8'))

    # build response with file
    response = HttpResponse(FileWrapper(xml_data_file), content_type='application/xml')
    response['Content-Disposition'] = 'attachment; filename=' + curate_data_structure.name
    return response


@decorators.permission_required(content_type=rights.curate_content_type,
                                permission=rights.curate_access, login_url=reverse_lazy("core_website_login"))
def download_xsd(request, curate_data_structure_id):
    """Makes the current XSD available for download.

    Args:
        request:
        curate_data_structure_id:

    Returns:

    """
    # get curate data structure
    curate_data_structure = data_structure_api.get_by_id(curate_data_structure_id)
    # check ownership
    _check_owner(request, accessed_object=curate_data_structure)

    # get the template
    template = curate_data_structure.template
    # build a file
    # TODO: test encoding
    template_file = StringIO(template.content.encode('utf-8'))

    # build response with file
    response = HttpResponse(FileWrapper(template_file), content_type='application/xsd')
    response['Content-Disposition'] = 'attachment; filename=' + template.filename

    return response


@decorators.permission_required(content_type=rights.curate_content_type,
                                permission=rights.curate_access, login_url=reverse_lazy("core_website_login"))
def generate_form(request, xsd_string, xml_string=None):
    """Generates the form using the parser, returns the root element

    Args:
        request:
        xsd_string:
        xml_string:

    Returns:

    """
    # build parser
    parser = get_parser()
    # generate form
    root_element_id = parser.generate_form(request, xsd_string, xml_string)
    # get the root element
    root_element = data_structure_element_api.get_by_id(root_element_id)

    return root_element


@decorators.permission_required(content_type=rights.curate_content_type,
                                permission=rights.curate_access, login_url=reverse_lazy("core_website_login"))
def render_form(request, root_element):
    """Renders the form

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


@decorators.permission_required(content_type=rights.curate_content_type,
                                permission=rights.curate_access, login_url=reverse_lazy("core_website_login"))
def render_xml(root_element):
    """Renders the XML

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
    """Updates the data structure with a root element

    Args:
        curate_data_structure:
        root_element:

    Returns:

    """
    # set the root element in the data structure
    curate_data_structure.data_structure_element_root = root_element
    # reset form string
    curate_data_structure.form_string = None
    # save the data structure
    data_structure_api.upsert(curate_data_structure)


def _read_file_content(file_path):
    """Reads the content of a file

    Args:
        file_path:

    Returns:

    """
    with open(file_path) as _file:
        file_content = _file.read()
        return file_content


# FIXME: make this check more general
def _check_owner(request, accessed_object):
    """Check if the object can be accessed by the user

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
