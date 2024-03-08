"""AJAX views for the Curate app
"""
import json
import logging

from django.contrib import messages
from django.http.response import HttpResponseBadRequest, HttpResponse
from django.template import loader
from django.urls import reverse
from django.utils.html import escape
from lxml.etree import XMLSyntaxError

import core_curate_app.components.curate_data_structure.api as curate_data_structure_api
import core_curate_app.views.user.forms as users_forms
from core_curate_app.common import exceptions as exceptions
from core_curate_app.common.exceptions import CurateAjaxError
from core_curate_app.components.curate_data_structure.models import (
    CurateDataStructure,
)
from core_curate_app.permissions import rights as rights
from core_curate_app.utils.parser import get_parser
from core_curate_app.views.user import views as curate_user_views
from core_main_app.commons.exceptions import JSONError
from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.components.lock import api as lock_api
from core_main_app.components.template import api as template_api
from core_main_app.components.template.models import Template
from core_main_app.utils import decorators
from core_main_app.utils import xml as main_xml_utils
from core_main_app.utils import json_utils as main_json_utils
from core_main_app.utils.json_utils import format_content_json
from core_main_app.utils.labels import get_data_label, get_form_label
from core_main_app.views.common import views as main_common_views
from core_parser_app.components.data_structure_element import (
    api as data_structure_element_api,
)
from core_parser_app.tools.parser.parser import remove_child_element
from core_parser_app.tools.parser.renderer.list import ListRenderer
from xml_utils.xsd_tree.xsd_tree import XSDTree

logger = logging.getLogger(__name__)


# FIXME: delete_branch not deleting all elements
# FIXME: generate element not testing max occurrences


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
    raise_exception=True,
)
def start_curate(request):
    """Load forms to start curating.

    Args:
        request:

    Returns:

    """
    try:
        if request.method == "POST":
            return _start_curate_post(request)

        return _start_curate_get(request)
    except CurateAjaxError as exception:
        return HttpResponseBadRequest(escape(str(exception)))
    except Exception as exception:
        return HttpResponseBadRequest(escape(str(exception)))


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
    raise_exception=True,
)
def generate_choice(request, curate_data_structure_id):
    """Generate a choice branch absent from the form.

    Args:
        request:
        curate_data_structure_id:

    Returns:

    """
    try:
        element_id = request.POST["id"]
        curate_data_structure = curate_data_structure_api.get_by_id(
            curate_data_structure_id, request.user
        )
        xsd_parser = get_parser(request=request)
        template = template_api.get_by_id(
            str(curate_data_structure.template.id), request=request
        )
        # check if xsd template
        if template.format != Template.XSD:
            return HttpResponseBadRequest("Template format not supported.")
        html_form = xsd_parser.generate_choice_absent(
            element_id, template.content, data_structure=curate_data_structure
        )
    except Exception as exception:
        return HttpResponseBadRequest(escape(str(exception)))

    return HttpResponse(html_form)


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
    raise_exception=True,
)
def generate_element(request, curate_data_structure_id):
    """Generate an element absent from the form.

    Args:
        request:
        curate_data_structure_id:

    Returns:

    """
    try:
        element_id = request.POST["id"]
        curate_data_structure = curate_data_structure_api.get_by_id(
            curate_data_structure_id, request.user
        )
        xsd_parser = get_parser(request=request)
        template = template_api.get_by_id(
            str(curate_data_structure.template.id), request=request
        )
        # check if xsd template
        if template.format != Template.XSD:
            return HttpResponseBadRequest("Template format not supported.")
        html_form = xsd_parser.generate_element_absent(
            element_id, template.content, data_structure=curate_data_structure
        )
    except Exception as exception:
        return HttpResponseBadRequest(escape(str(exception)))

    return HttpResponse(html_form)


# TODO: need to be reworked
@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
    raise_exception=True,
)
def remove_element(request):
    """Remove an element from the form.

    Args:
        request:

    Returns:

    """
    element_id = request.POST["id"]

    # Removing the element from the data structure
    data_structure_element_to_pull = data_structure_element_api.get_by_id(
        element_id, request
    )
    data_structure_element = data_structure_element_to_pull.parent

    # number of children after deletion
    children_number = data_structure_element.children.count() - 1

    data_structure_element = remove_child_element(
        data_structure_element, data_structure_element_to_pull, request
    )

    response = {"code": 0, "html": ""}

    if children_number > data_structure_element.options["min"]:
        return HttpResponse(json.dumps(response))

    # len(schema_element.children) == schema_element.options['min']
    if data_structure_element.options["min"] != 0:
        response["code"] = 1
    else:  # schema_element.options['min'] == 0
        renderer = ListRenderer(data_structure_element, request)
        html_form = renderer.render(True)

        response["code"] = 2
        response["html"] = html_form

    return HttpResponse(json.dumps(response))


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
    raise_exception=True,
)
def clear_fields(request):
    """Clear fields of the current form.

    Args:
        request:

    Returns:

    """
    try:
        # get curate data structure
        curate_data_structure_id = request.POST["id"]
        curate_data_structure = curate_data_structure_api.get_by_id(
            curate_data_structure_id, request.user
        )

        # generate form
        template = template_api.get_by_id(
            str(curate_data_structure.template.id), request=request
        )
        # check if xsd template
        if template.format != Template.XSD:
            return HttpResponseBadRequest("Template format not supported.")

        root_element = curate_user_views.generate_form(
            template.content,
            data_structure=curate_data_structure,
            request=request,
        )

        # save the root element in the data structure
        curate_data_structure_api.update_data_structure_root(
            curate_data_structure, root_element, request.user
        )

        # renders the form
        xsd_form = curate_user_views.render_form(request, root_element)

        return HttpResponse(
            json.dumps({"xsdForm": xsd_form}),
            content_type="application/javascript",
        )
    except Exception as exception:
        return HttpResponseBadRequest(escape(str(exception)))


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
    raise_exception=True,
)
def cancel_changes(request):
    """Cancel changes of the current form.

    Args:
        request:

    Returns:

    """
    try:
        # get curate data structure
        curate_data_structure_id = request.POST["id"]
        curate_data_structure = curate_data_structure_api.get_by_id(
            curate_data_structure_id, request.user
        )

        if curate_data_structure.data is not None:
            # data already saved, reload from data
            content = curate_data_structure.data.content
        elif curate_data_structure.form_string is not None:
            # form already saved, reload from saved form
            content = curate_data_structure.form_string
        else:
            # no saved data, load new form
            content = None

        if curate_data_structure.template.format == Template.XSD:
            root_element = curate_user_views.generate_root_element(
                request, curate_data_structure, content
            )

            # renders the form
            xsd_form = curate_user_views.render_form(request, root_element)
            result = {"xsdForm": xsd_form}
        elif curate_data_structure.template.format == Template.JSON:
            result = {"content": content}
        else:
            return HttpResponseBadRequest("Template format not supported.")

        return HttpResponse(
            json.dumps(result),
            content_type="application/javascript",
        )
    except Exception as exception:
        return HttpResponseBadRequest(escape(str(exception)))


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
    raise_exception=True,
)
def cancel_form(request):
    """Cancel current form.

    Args:
        request:

    Returns:

    """
    try:
        # get curate data structure
        curate_data_structure_id = request.POST["id"]
        curate_data_structure = curate_data_structure_api.get_by_id(
            curate_data_structure_id, request.user
        )
        # unlock from database
        if curate_data_structure.data is not None:
            lock_api.remove_lock_on_object(
                curate_data_structure.data, request.user
            )
        curate_data_structure_api.delete(curate_data_structure, request.user)

        # add success message
        messages.add_message(
            request,
            messages.SUCCESS,
            get_form_label().capitalize() + " deleted with success.",
        )

        return HttpResponse(json.dumps({}), content_type="application/json")
    except Exception as exception:
        error_message = (
            "An unexpected error has occurred while cancelling "
            f"the {get_form_label()}"
        )

        logger.error("%s: %s", error_message, str(exception))
        return HttpResponseBadRequest(
            json.dumps({"error": error_message}),
            content_type="application/json",
        )


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
    raise_exception=True,
)
def save_form(request):
    """Save the current form in data base. Converts it to XML format first.

    Args:
        request:

    Returns:

    """
    try:
        # get curate data structure
        curate_data_structure_id = request.POST["id"]
        curate_data_structure = curate_data_structure_api.get_by_id(
            curate_data_structure_id, request.user
        )

        if curate_data_structure.template.format == Template.XSD:
            form_string = request.POST.get("form_string", None)
            if form_string is None:
                form_string = curate_user_views.render_xml(
                    request,
                    curate_data_structure.data_structure_element_root,
                )
            else:
                # check if form string is well formed
                main_xml_utils.format_content_xml(form_string)

        elif curate_data_structure.template.format == Template.JSON:
            form_string = request.POST.get("form_string", "{}")
            # check if form string is well formed
            format_content_json(form_string)
        else:
            return HttpResponseBadRequest("Template format not supported.")

        # update curate data structure data
        curate_data_structure.form_string = form_string

        # save data structure
        curate_data_structure_api.upsert(curate_data_structure, request.user)

        return HttpResponse(
            json.dumps(
                {
                    "message": f"{get_form_label().capitalize()} saved with success."
                }
            ),
            content_type="application/json",
        )
    except Exception as exception:
        error_message = (
            f"An error occurred while saving the {get_form_label()}"
        )
        logger.error("%s: %s", error_message, str(exception))
        return HttpResponseBadRequest(
            json.dumps({"error": error_message, "details": str(exception)}),
            content_type="application/json",
        )


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
    raise_exception=True,
)
def validate_form(request):
    """Validate data present in the form via XML validation.

    Args:
        request:

    Returns:

    """
    response_dict = {}
    try:
        # get curate data structure
        curate_data_structure_id = request.POST["id"]
        curate_data_structure = curate_data_structure_api.get_by_id(
            curate_data_structure_id, request.user
        )
        # get template
        template = template_api.get_by_id(
            str(curate_data_structure.template.id), request=request
        )
        # check if xsd template
        if template.format == Template.XSD:
            # generate the XML
            xml_data = curate_user_views.render_xml(
                request, curate_data_structure.data_structure_element_root
            )
            # build trees
            xsd_tree = XSDTree.build_tree(template.content)
            form_string = XSDTree.build_tree(xml_data)

            # validate XML document
            errors = main_xml_utils.validate_xml_data(
                xsd_tree, form_string, request=request
            )
            if errors is not None:
                response_dict["errors"] = errors
        elif template.format == Template.JSON:
            try:
                main_json_utils.validate_json_data(
                    request.POST["form_string"]
                    if "form_string" in request.POST
                    else curate_data_structure.form_string,
                    template.content,
                )
            except JSONError as json_error:
                response_dict["errors"] = [
                    escape(str(message)) for message in json_error.message_list
                ]
        else:
            return HttpResponseBadRequest("Template format not supported.")

    except XMLSyntaxError as xml_syntax_error:
        response_dict[
            "errors"
        ] = "Your XML data is not well formatted. " + str(xml_syntax_error)
    except Exception as exception:
        message = (
            str(exception).replace('"', "'")
            if str(exception) is not None
            else "The current document cannot be validated."
        )
        response_dict["errors"] = message

    return HttpResponse(
        json.dumps(response_dict), content_type="application/javascript"
    )


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
    raise_exception=True,
)
def save_data(request):
    """Save data - delete curate data structure.

    Args:
        request:

    Returns:

    """
    try:
        # get curate data structure
        curate_data_structure_id = request.POST["id"]
        curate_data_structure = curate_data_structure_api.get_by_id(
            curate_data_structure_id, request.user
        )

        # unlock from database
        if curate_data_structure.data is not None:
            lock_api.remove_lock_on_object(
                curate_data_structure.data, request.user
            )

        if curate_data_structure.template.format == Template.XSD:
            # generate the XML
            form_string = curate_user_views.render_xml(
                request, curate_data_structure.data_structure_element_root
            )
        elif curate_data_structure.template.format == Template.JSON:
            form_string = curate_data_structure.form_string
        else:
            return HttpResponseBadRequest("Template format not supported.")

        if curate_data_structure.data is not None:
            # update existing data
            data = curate_data_structure.data
        else:
            # create new data
            data = Data()
            data.title = curate_data_structure.name
            template = template_api.get_by_id(
                str(curate_data_structure.template.id), request=request
            )
            data.template = template
            data.user_id = str(request.user.id)

        # set content
        data.content = form_string
        # save data
        data = data_api.upsert(data, request)

        curate_data_structure_api.delete(curate_data_structure, request.user)

        messages.add_message(
            request,
            messages.SUCCESS,
            get_data_label().capitalize() + " saved with success.",
        )
    except Exception as exception:
        return HttpResponseBadRequest(
            str(exception).replace('"', "'"),
            content_type="application/javascript",
        )

    return HttpResponse(
        json.dumps({"data_id": str(data.id)}),
        content_type="application/javascript",
    )


def _start_curate_post(request):
    """Start curate POST request.

    Args:
        request:

    Returns:

    """
    template_id = str(request.POST["template_id"])
    selected_option = request.POST["curate_form"]
    user_id = str(request.user.id)

    if selected_option == "new":
        new_form = users_forms.NewForm(request.POST)
        if not new_form.is_valid():
            raise CurateAjaxError(
                "An error occurred during the validation " + get_form_label()
            )
        name = new_form.data["document_name"]
        template = template_api.get_by_id(template_id, request=request)
        # check template format
        if (
            template.format != Template.XSD
            and template.format != Template.JSON
            and "text_editor" not in new_form.data
        ):
            return HttpResponseBadRequest("Template format not supported.")
        curate_data_structure = CurateDataStructure(
            user=user_id,
            template=template,
            name=name,
        )
        curate_data_structure_api.upsert(curate_data_structure, request.user)
        url = _get_reverse_url(new_form, curate_data_structure.id)
    elif selected_option == "upload":
        upload_form = users_forms.UploadForm(request.POST, request.FILES)
        if not upload_form.is_valid():
            raise CurateAjaxError(
                f"An error occurred during the file upload: {upload_form.errors.as_text()}"
            )
        # get template
        template = template_api.get_by_id(
            template_id,
            request=request,
        )
        file = request.FILES["file"]
        name = file.name
        # check template format
        if template.format == Template.XSD:
            content = main_common_views.read_xsd_file(file)
            well_formed = main_xml_utils.is_well_formed_xml(content)
        elif template.format == Template.JSON:
            content = file.read().decode("utf-8")
            well_formed = main_json_utils.is_well_formed_json(content)
        else:
            return HttpResponseBadRequest("Template format not supported.")
        if not well_formed:
            return HttpResponseBadRequest(
                "An error occurred during the file upload: the file is "
                "not well formed " + template.format
            )
        if (
            "direct_upload" in upload_form.data
            and upload_form.data["direct_upload"]
        ):
            # create data
            data = Data(
                title=name, template=template, user_id=str(request.user.id)
            )
            # set content
            data.content = content
            # save data
            data_api.upsert(data, request)
            messages.add_message(
                request,
                messages.SUCCESS,
                get_data_label().capitalize() + " saved with success.",
            )
            url = reverse("core_main_app_data_detail") + f"?id={str(data.id)}"
        else:
            curate_data_structure = CurateDataStructure(
                user=user_id,
                template=template_api.get_by_id(template_id, request=request),
                name=name,
                form_string=content,
            )
            curate_data_structure_api.upsert(
                curate_data_structure, request.user
            )
            url = _get_reverse_url(upload_form, curate_data_structure.id)
    else:
        open_form = users_forms.OpenForm(request.POST)
        curate_data_structure = curate_data_structure_api.get_by_id(
            open_form.data["forms"], request.user
        )
        url = _get_reverse_url(open_form, curate_data_structure.id)
    return HttpResponse(url)


def _get_reverse_url(form, curate_data_structure_id):
    """get reverse url.
    Args:
        form:
        curate_data_structure_id
    Returns:
        url:
    """
    if "text_editor" in form.data:
        if form.data["template_format"] == Template.JSON:
            url = (
                reverse("core_curate_app_json_text_editor_view")
                + f"?id={str(curate_data_structure_id)}"
            )
        else:
            url = (
                reverse("core_curate_app_xml_text_editor_view")
                + f"?id={str(curate_data_structure_id)}"
            )
    else:
        url = reverse(
            "core_curate_enter_data", args=(curate_data_structure_id,)
        )
    return url


def _start_curate_get(request):
    """Start curate GET request.

    Args:
        request:

    Returns:

    """
    try:
        context_params = dict()
        template_id = request.GET["template_id"]
        template = loader.get_template(
            "core_curate_app/user/curate_start.html"
        )

        open_form = users_forms.OpenForm(
            forms=curate_data_structure_api.get_all_by_user_id_and_template_id_with_no_data(
                request.user.id, template_id
            )
        )
        new_form = users_forms.NewForm()
        upload_form = users_forms.UploadForm()
        hidden_form = users_forms.HiddenFieldsForm(
            template_id=template_id,
            template_format=template_api.get_by_id(
                template_id, request=request
            ).format,
        )
        context_params["new_form"] = new_form
        context_params["open_form"] = open_form
        context_params["upload_form"] = upload_form
        context_params["hidden_form"] = hidden_form
        context_params["request"] = request
        context = {}

        context.update(context_params)
        return HttpResponse(
            json.dumps({"template": template.render(context)}),
            content_type="application/javascript",
        )
    except Exception as exception:
        logger.error(str(exception))
        raise exceptions.CurateAjaxError(
            "Error occurred during the " + get_form_label() + " display."
        )
