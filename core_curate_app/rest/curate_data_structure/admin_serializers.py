"""Curate Data Structure Serializers
"""
from rest_framework.serializers import ModelSerializer

from core_curate_app.components.curate_data_structure import (
    api as curate_data_structure_api,
)
from core_curate_app.components.curate_data_structure.models import (
    CurateDataStructure,
)


class CurateDataStructureAdminSerializer(ModelSerializer):
    """CurateDataStructure Serializer"""

    class Meta:
        """Meta"""

        model = CurateDataStructure
        fields = "__all__"

    def create(self, validated_data):
        """
        Create and return a new `CurateDataStructure` instance, given the validated data.
        """
        # Create data
        curate_data_structure = CurateDataStructure(
            user=validated_data["user"],
            name=validated_data["name"],
            template=validated_data["template"],
            form_string=validated_data["form_string"]
            if "form_string" in validated_data
            else None,
            data=validated_data["data"] if "data" in validated_data else None,
            data_structure_element_root=validated_data[
                "data_structure_element_root"
            ]
            if "data_structure_element_root" in validated_data
            else None,
        )
        return curate_data_structure_api.upsert(
            curate_data_structure, self.context["request"].user
        )
