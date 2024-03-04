"""
    Common views
"""
import json

from django.contrib import messages
from django.http import (
    HttpResponseBadRequest,
    HttpResponseForbidden,
    HttpResponse,
)
from django.urls import reverse
from django.utils.html import escape as html_escape
from django.utils.translation import gettext as _

from core_curate_app.components.curate_data_structure import (
    api as data_structure_api,
)
from core_main_app.commons import exceptions

from core_main_app.utils import file as main_file_utils
from core_curate_app.views.user.views import _get_curate_data_structure_by_id
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import (
    DoesNotExist,
    JSONError,
)
from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.components.template import api as template_api
from core_main_app.settings import MAX_DOCUMENT_EDITING_SIZE

from core_main_app.utils.labels import get_data_label, get_form_label
from core_main_app.views.common.views import CommonView, XmlEditor, JSONEditor
from core_curate_app.access_control import api as acl_api


class FormView(CommonView):
    """
    Form View
    """

    template = "core_curate_app/user/detail.html"

    def get(self, request, *args, **kwargs):
        """Get the web page of a given form

        Args:
            request:

        Returns:
        """
        try:
            # get data structure
            curate_data_structure = _get_curate_data_structure_by_id(
                kwargs["curate_data_structure_id"], request
            )

            # TODO: fix with the rework on the curate workflow
            if (
                curate_data_structure.form_string is None
                or curate_data_structure.form_string == ""
            ):
                raise Exception(
                    "The "
                    + _("form_label")
                    + " was not saved and cannot be displayed."
                )

            # Set the assets
            assets = {
                "js": [
                    {
                        "path": "core_main_app/common/js/XMLTree.js",
                        "is_raw": False,
                    },
                    {
                        "path": "core_main_app/user/js/data/detail.js",
                        "is_raw": False,
                    },
                ],
                "css": ["core_main_app/common/css/XMLTree.css"],
            }

            # Set the context
            context = {
                "data_structure": curate_data_structure,
                "page_title": "View Form",
            }

            return self.common_render(
                request, self.template, assets=assets, context=context
            )
        except Exception as exception:
            assets = {
                "js": [
                    {
                        "path": "core_main_app/user/js/data/detail.js",
                        "is_raw": False,
                    },
                ]
            }
            template = "core_main_app/common/commons/error.html"
            if self.administration:
                template = (
                    "core_main_app/admin/commons/errors/errors_wrapper.html"
                )

            return self.common_render(
                request,
                template,
                context={"error": str(exception), "page_title": "Error"},
                assets=assets,
            )


class DataStructureMixin:
    object_name = get_form_label()

    def _get_object(self, request):
        """get object

        Args:
            request

        Returns:
        """
        return data_structure_api.get_by_id(request.GET["id"], request.user)

    def _check_permission(self, data_structure, request):
        """check user permission
        Args:
            data_structure:
            request:
        Returns:
        """
        return acl_api.check_can_write(data_structure, request.user)

    def _check_size(self, data_structure):
        """check content size

        Args:
            data_structure:

        Returns:
        """

        if (
            main_file_utils.get_byte_size_from_string(
                data_structure.form_string
            )
            > MAX_DOCUMENT_EDITING_SIZE
        ):
            raise exceptions.DocumentEditingSizeError(
                "The file is too large (MAX_DOCUMENT_EDITING_SIZE)."
            )

    def _get_assets(self):
        """get assestd

        Args:

        Returns:
        """
        assets = super()._get_assets()
        # add js relatives to the data structure editor
        assets["js"].append(
            {
                "path": "core_curate_app/user/js/text_editor.raw.js",
                "is_raw": True,
            },
        )
        assets["js"].append(
            {
                "path": "core_curate_app/user/js/switch_editor.js",
                "is_raw": False,
            },
        )

        return assets

    def _get_modals(self):
        """get modals

        Args:

        Return:
        """

        # add modals relatives to the data structure editor
        return [
            "core_main_app/common/modals/create_data_modal.html",
            "core_curate_app/user/data-entry/modals/switch_to_form_editor.html",
        ]

    def save(self, *args, **kwargs):
        """Save as data
        Args:
            *args:
            **kwargs:
        Returns:
        """
        try:
            request = kwargs.get("request")
            content = request.POST["content"].strip()
            data_structure_id = request.POST["document_id"]
            data_structure = data_structure_api.get_by_id(
                data_structure_id, request.user
            )
            if data_structure.data is not None:
                data = data_structure.data
            else:
                # create new data
                data = Data()
                data.title = data_structure.name
                template = template_api.get_by_id(
                    str(data_structure.template.id), request=request
                )
                data.template = template
                data.user_id = str(request.user.id)

            # set content
            data.content = content
            # save data
            data_api.upsert(data, request)
            data_structure_api.delete(data_structure, request.user)
            messages.add_message(
                request,
                messages.SUCCESS,
                get_data_label().capitalize() + " saved with success.",
            )
            return HttpResponse(
                json.dumps({"url": reverse("core_curate_index")}),
                "application/javascript",
            )
        except AccessControlError as ace:
            return HttpResponseForbidden(html_escape(str(ace)))
        except DoesNotExist as dne:
            return HttpResponseBadRequest(html_escape(str(dne)))
        except JSONError as json_error:
            return HttpResponseBadRequest(
                json.dumps(
                    [
                        html_escape(str(message))
                        for message in json_error.message_list
                    ]
                )
            )
        except Exception as e:
            return HttpResponseBadRequest(html_escape(str(e)))


class DataStructureXMLEditor(DataStructureMixin, XmlEditor):
    """Data Structure XML Editor View"""

    def _prepare_context(self, data_structure):
        """prepare context
        Args:
            data_structure:

        Returns:
        """
        return self.get_context(
            data_structure, data_structure.name, data_structure.form_string
        )


class DataStructureJSONEditor(DataStructureMixin, JSONEditor):
    """Data Structure JSON Editor View"""

    def _prepare_context(self, data_structure):
        """prepare context

        Args:
            data_structure:

        Returns:
        """
        return self.get_context(
            data_structure, data_structure.name, data_structure.form_string
        )
