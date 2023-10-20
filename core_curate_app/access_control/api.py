""" Set of functions to define the common rules for access control across collections
"""
import logging

from django.contrib.auth.models import User, AnonymousUser
from core_main_app.access_control.exceptions import AccessControlError
from core_curate_app.components.curate_data_structure.models import (
    CurateDataStructure,
)

logger = logging.getLogger(__name__)


def can_read(func, *args, **kwargs):
    """Can user read

    Args:
        func:
        *args:
        **kwargs:

    Returns:

    """
    # get the User in the args list
    user = next(
        (arg for arg in args if isinstance(arg, (User, AnonymousUser))),
        None,
    )

    if user.is_anonymous or user is None:
        raise AccessControlError(
            "The user doesn't have enough rights to access this document."
        )

    if user.is_superuser:
        return func(*args, **kwargs)

    document = func(*args, **kwargs)
    if isinstance(document, list):
        document_list = document
    elif isinstance(document, CurateDataStructure):
        document_list = [document]
    else:
        document_list = list(document)

    _check_can_read(document_list, user)

    return document


def _check_can_read(document_list, user):
    """Can read from list id.

    Args:
        document_list:
        user:

    Returns:

    """
    # check access is correct
    for document in document_list:
        # user is document owner
        if document.user == str(user.id):
            continue
        # user is not owner or document
        raise AccessControlError("The user doesn't have enough rights.")


def check_can_write(data_structure, user):
    """Check that the user can write.

    Args:
        data_structure:
        user:

    Returns:

    """

    if user is None or user.is_anonymous:
        raise AccessControlError(
            "The user doesn't have enough rights to access this document."
        )
    if user.is_superuser:
        return

    if data_structure.user != str(user.id):
        raise AccessControlError(
            "The user doesn't have enough rights to access this document."
        )

    return


def can_write(func, *args, **kwargs):
    """Can user write

    Args:
        func:
        *args:
        **kwargs:

    Returns:

    """
    user = next(
        (arg for arg in args if isinstance(arg, (User, AnonymousUser))),
        None,
    )
    data_structure = next(
        (arg for arg in args if isinstance(arg, CurateDataStructure)), None
    )

    check_can_write(data_structure, user)
    return func(*args, **kwargs)


def can_change_owner(func, document, new_user, user):
    """Can user change document's owner.

    Args:
        func:
        document:
        new_user:
        user:

    Returns:

    """
    if user.is_anonymous:
        raise AccessControlError(
            "The user doesn't have enough rights to access this document."
        )
    if user.is_superuser:
        return func(document, new_user, user)

    if document.user == str(user.id):
        return func(document, new_user, user)

    raise AccessControlError(
        "The user doesn't have enough rights to access this document."
    )
