""" Custom admin site for the Curate Data Structure model
"""
from django.contrib import admin


class CustomCurateDataStructureAdmin(admin.ModelAdmin):
    """CustomCurateDataStructureAdmin"""

    readonly_fields = ["template", "data_structure_element_root", "form_string", "data"]

    def has_add_permission(self, request, obj=None):
        """Prevent from manually adding Curate Data Structures"""
        return False
