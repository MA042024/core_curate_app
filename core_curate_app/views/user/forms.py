""" User curate forms
"""
from django import forms
from django.conf import settings

from core_main_app.commons.constants import (
    DATA_FILE_EXTENSION_FOR_TEMPLATE_FORMAT,
)
from core_main_app.settings import MAX_DOCUMENT_EDITING_SIZE
from core_main_app.utils.labels import get_form_label
import core_curate_app.components.curate_data_structure.api as curate_data_structure_api
from django.core.exceptions import ValidationError


class NewForm(forms.Form):
    """Form to start curating from an empty form."""

    document_name = forms.CharField(
        label="",
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )


class FormDataModelChoiceField(forms.ModelChoiceField):
    """Choice Field to select an existing form."""

    def label_from_instance(self, obj):
        """Return label.

        Args:
            obj:

        Returns:

        """
        return obj.name


class OpenForm(forms.Form):
    """Form to open an existing form."""

    forms = FormDataModelChoiceField(
        label="",
        queryset=curate_data_structure_api.get_none(),
        widget=forms.Select(),
    )

    def __init__(self, *args, **kwargs):
        if "forms" in kwargs:
            queryset = kwargs.pop("forms")
        else:
            queryset = curate_data_structure_api.get_none()
        super().__init__(*args, **kwargs)
        self.fields["forms"].queryset = queryset
        if settings.BOOTSTRAP_VERSION.startswith("4"):
            self.fields["forms"].widget.attrs["class"] = "form-control"
        elif settings.BOOTSTRAP_VERSION.startswith("5"):
            self.fields["forms"].widget.attrs["class"] = "form-select"


def _file_size_validator(value):
    """Check size of uploaded file

    Args:
        value:

    Returns:

    """
    if value.size > MAX_DOCUMENT_EDITING_SIZE:
        raise ValidationError(
            "The file is too large (MAX_DOCUMENT_EDITING_SIZE)."
        )


class UploadForm(forms.Form):
    """Form to start curating from a file."""

    file = forms.FileField(
        label="",
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "accept": ",".join(
                    DATA_FILE_EXTENSION_FOR_TEMPLATE_FORMAT.values()
                ),
            }
        ),
        validators=[_file_size_validator],
    )
    direct_upload = forms.BooleanField(
        label="",
        widget=forms.CheckboxInput(attrs={"hidden": "true"}),
        required=False,
    )
    text_editor = forms.BooleanField(
        label="",
        widget=forms.CheckboxInput(attrs={"hidden": "true"}),
        required=False,
    )


class CancelChangesForm(forms.Form):
    """Cancel changes form."""

    CANCEL_CHOICES = [
        ("revert", "Revert to my previously Saved " + get_form_label()),
        ("return", "Return to Add Resources"),
    ]

    cancel = forms.ChoiceField(
        label="", choices=CANCEL_CHOICES, widget=forms.RadioSelect()
    )


class HiddenFieldsForm(forms.Form):
    """Form for hidden fields."""

    template_id = forms.CharField(widget=forms.HiddenInput(), required=True)
    template_format = forms.CharField(
        widget=forms.HiddenInput(), required=True
    )

    def __init__(self, *args, **kwargs):
        template_id = ""
        template_format = ""
        if "template_id" in kwargs:
            template_id = kwargs.pop("template_id")
        if "template_format" in kwargs:
            template_format = kwargs.pop("template_format")
        super().__init__(*args, **kwargs)
        self.fields["template_id"].initial = template_id
        self.fields["template_format"].initial = template_format
