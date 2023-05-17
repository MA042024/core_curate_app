"""Admin AJAX views for the Curate app
"""

import json

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.messages.storage.base import Message
from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
)

import core_main_app.components.data.api as data_api

from core_main_app.commons.exceptions import DoesNotExist

from core_main_app.utils.labels import get_data_label

import core_curate_app.components.curate_data_structure.api as curate_data_structure_api


@staff_member_required
def delete_record_drafts(request, pk):
    """Delete record drafts.

    Args:
        request:
        pk:

    Returns:
    """
    try:
        # Get data
        data = data_api.get_by_id(pk, request.user)

        # delete curate data structures
        curate_data_structure_api.delete_curate_data_structures_by_data(
            data, request.user
        )

        message = Message(
            messages.SUCCESS,
            "Drafts deleted with success",
        )
    except DoesNotExist:
        message = Message(
            messages.ERROR,
            "It seems a "
            + get_data_label()
            + " is missing. Please refresh the page.",
        )
        return HttpResponseBadRequest(
            json.dumps({"message": message.message, "tags": message.tags}),
            content_type="application/json",
        )
    except Exception:
        message = Message(messages.ERROR, "A problem occurred while deleting.")
        return HttpResponseBadRequest(
            json.dumps({"message": message.message, "tags": message.tags}),
            content_type="application/json",
        )

    return HttpResponse(
        json.dumps({"message": message.message, "tags": message.tags}),
        content_type="application/json",
    )
