"""Url router for the REST API
"""

from django.urls import re_path

from core_curate_app.rest.curate_data_structure.views import (
    AdminCurateDataStructureList,
)

urlpatterns = [
    re_path(
        r"^admin/draft/$",
        AdminCurateDataStructureList.as_view(),
        name="core_curate_app_rest_drafts",
    ),
]
