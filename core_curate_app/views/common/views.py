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
from django.utils.translation import ugettext as _

from core_curate_app.components.curate_data_structure import (
    api as data_structure_api,
)
from core_curate_app.views.user.views import _get_curate_data_structure_by_id
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import (
    DoesNotExist,
    DocumentEditingSizeError,
)
from core_main_app.components.data import api as data_api
from core_main_app.components.data.models import Data
from core_main_app.components.template import api as template_api
from core_main_app.settings import MAX_DOCUMENT_EDITING_SIZE
from core_main_app.utils import file as main_file_utils
from core_main_app.utils.labels import get_data_label
from core_main_app.utils.rendering import render
from core_main_app.views.common.views import CommonView, XmlEditor


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
            if curate_data_structure.form_string is None:
                raise Exception(
                    "The "
                    + _("form_label")
                    + " was not saved. We can't display the correct data."
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
                        "path": "core_main_app/common/js/backtoprevious.js",
                        "is_raw": True,
                    }
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


class DraftContentEditor(XmlEditor):
    """Draft Content Editor View"""

    def get(self, request):
        """get

        Args:
            request

        Returns:
        """

        try:

            data_structure = data_structure_api.get_by_id(
                request.GET["id"], request.user
            )
            if (
                main_file_utils.get_byte_size_from_string(
                    data_structure.form_string
                )
                > MAX_DOCUMENT_EDITING_SIZE
            ):
                raise DocumentEditingSizeError(
                    "The file is too large (MAX_DOCUMENT_EDITING_SIZE)."
                )
            context = self.get_context(
                data_structure, data_structure.name, data_structure.form_string
            )
            assets = self._get_assets()
            modals = ["core_main_app/common/modals/create_data_modal.html"]
            return render(
                request,
                self.template,
                assets=assets,
                context=context,
                modals=modals,
            )
        except AccessControlError:
            error_message = "Access Forbidden"
            status_code = 403
        except DoesNotExist:
            error_message = "Form not found"
            status_code = 404
        except Exception as e:
            error_message = str(e)
            status_code = 400

        return render(
            request,
            "core_main_app/common/commons/error.html",
            assets={
                "js": [
                    {
                        "path": "core_main_app/user/js/data/detail.js",
                        "is_raw": False,
                    }
                ]
            },
            context={
                "error": error_message,
                "status_code": status_code,
            },
        )

    def save(self, *args, **kwargs):
        """Save xml content

        Args:
            args:
            kwargs:

        Returns:

        """
        try:
            content = self.request.POST["content"].strip()
            data_structure_id = self.request.POST["document_id"]
            data_structure = data_structure_api.get_by_id(
                data_structure_id, self.request.user
            )

            # create new data
            data = Data()
            data.title = data_structure.name
            template = template_api.get_by_id(
                str(data_structure.template.id), request=self.request
            )
            data.template = template
            data.user_id = str(self.request.user.id)

            # set content
            data.xml_content = content
            # save data
            data = data_api.upsert(data, self.request)

            data_structure_api.delete(data_structure, self.request.user)
            messages.add_message(
                self.request,
                messages.SUCCESS,
                get_data_label() + " saved with success.",
            )
            return HttpResponse(
                json.dumps({"url": reverse(self.save_redirect)}),
                "application/javascript",
            )
        except AccessControlError as ace:
            return HttpResponseForbidden(html_escape(str(ace)))
        except DoesNotExist as dne:
            return HttpResponseBadRequest(html_escape(str(dne)))
        except Exception as e:
            return HttpResponseBadRequest(html_escape(str(e)))

    def _get_assets(self):
        assets = super()._get_assets()

        # add js relatives to the xml editor
        assets["js"].append(
            {
                "path": "core_curate_app/user/js/text_editor.raw.js",
                "is_raw": True,
            },
        )
        return assets
