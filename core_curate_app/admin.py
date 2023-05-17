"""
Url router for the administration site
"""
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import re_path

from core_main_app.admin import core_admin_site
from core_curate_app.components.curate_data_structure.admin_site import (
    CustomCurateDataStructureAdmin,
)
from core_curate_app.components.curate_data_structure.models import (
    CurateDataStructure,
)
from core_curate_app.views.common import views as common_views
from core_curate_app.views.admin import ajax as admin_ajax

admin_urls = [
    re_path(
        r"^view-form/(?P<curate_data_structure_id>\w+)$",
        staff_member_required(
            common_views.FormView.as_view(
                administration=True,
                template="core_curate_app/admin/view_curate_data_structure.html",
            )
        ),
        name="core_curate_view_form",
    ),
    re_path(
        r"^delete-record-drafts/(?P<pk>\w+)$",
        admin_ajax.delete_record_drafts,
        name="core_curate_app_delete_data_drafts",
    ),
]

admin.site.register(CurateDataStructure, CustomCurateDataStructureAdmin)
urls = core_admin_site.get_urls()
core_admin_site.get_urls = lambda: admin_urls + urls
