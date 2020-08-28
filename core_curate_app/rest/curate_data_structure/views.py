""" Views for the Curate Data Structure REST API
"""
import logging

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from core_main_app.access_control.exceptions import AccessControlError

from core_curate_app.components.curate_data_structure.models import CurateDataStructure
from core_curate_app.rest.curate_data_structure.serializers import (
    CurateDataStructureSerializer,
)
from core_main_app.commons import exceptions

logger = logging.getLogger(__name__)


class AdminCurateDataStructureList(APIView):
    """List all Curate Data Structure, or create a new one."""

    permission_classes = (IsAdminUser,)
    serializer = CurateDataStructureSerializer

    def get(self, request):
        """Get all user Curate Data Structure

        Args:

            request: HTTP request

        Returns:

            - code: 200
              content: List of curate data structure
            - code: 403
              content: Forbidden
            - code: 500
              content: Internal server error
        """
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            # Get object
            object_list = CurateDataStructure.get_all()

            # Serialize object
            serializer = self.serializer(object_list, many=True)

            # Return response
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        """Create a Curate Data Structure

        Parameters:

            {
                "user": "1",
                "name": "name",
                "form_string": "<xml></xml>",
                "template": "5eb1cc6d53d26cbd4085c722",
                "data_structure_element_root": "5eb36cc1b72a6298744d746a",
                "data": "5eb36ca0b72a6298744d724b"
            }

        Args:

            request: HTTP request

        Returns:

            - code: 201
              content: Created data
            - code: 400
              content: Validation error
            - code: 404
              content: Template was not found
            - code: 500
              content: Internal server error
        """
        if not request.user.is_superuser:
            return Response(status=status.HTTP_403_FORBIDDEN)

        try:
            # Build serializer
            serializer = self.serializer(data=request.data)

            # Validate data
            serializer.is_valid(True)
            # Save data
            serializer.save(user_request=request.user)

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except AccessControlError as e:
            content = {"message": str(e)}
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.DoesNotExist:
            content = {"message": "Object not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
