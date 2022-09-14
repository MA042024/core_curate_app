""" Views for the Curate Data Structure REST API
"""
import logging

from django.http import Http404
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons import exceptions
from core_curate_app.components.curate_data_structure import api as data_structure_api
from core_curate_app.components.curate_data_structure.models import CurateDataStructure
from core_curate_app.rest.curate_data_structure.admin_serializers import (
    CurateDataStructureAdminSerializer,
)
from core_curate_app.rest.curate_data_structure.serializers import (
    CurateDataStructureSerializer,
)

logger = logging.getLogger(__name__)


class AdminCurateDataStructureList(APIView):
    """List all Curate Data Structure, or create a new one."""

    permission_classes = (IsAdminUser,)
    serializer = CurateDataStructureAdminSerializer

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
            serializer = self.serializer(
                data=request.data, context={"request": request}
            )

            # Validate data
            serializer.is_valid(True)
            # Save data
            serializer.save()

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except AccessControlError as access_control_exception:
            content = {"message": str(access_control_exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.DoesNotExist:
            content = {"message": "Object not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CurateDataStructureList(APIView):
    """List Curate Data Structure by user, create a new one."""

    permission_classes = (IsAuthenticated,)
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
        try:
            # Get object
            object_list = data_structure_api.get_all_by_user(request.user)

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

        try:
            # Build serializer
            serializer = self.serializer(
                data=request.data, context={"request": request}
            )

            # Validate data
            serializer.is_valid(True)
            # Save data
            serializer.save()

            # Return the serialized data
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except exceptions.DoesNotExist:
            content = {"message": "Object not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CurateDataStructureDetail(APIView):
    """Retrieve, update or delete a Curate Data Structure"""

    permission_classes = (IsAuthenticated,)
    serializer = CurateDataStructureSerializer

    def get_object(self, request, pk):
        """Get Curate Data Structure from db

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            Data
        """
        try:
            return data_structure_api.get_by_id(pk, request.user)
        except exceptions.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """Retrieve a Curate Data Structure

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content:  Curate Data Structure
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            data_structure_object = self.get_object(request, pk)

            # Serialize object
            serializer = self.serializer(data_structure_object)

            # Return response
            return Response(serializer.data)
        except AccessControlError as access_control_exception:
            content = {"message": str(access_control_exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Http404:
            content = {"message": "Data structure not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk):
        """Delete a Curate Data Structure

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 204
              content: Deletion succeed
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            data_structure_object = self.get_object(request, pk)

            # delete object
            data_structure_api.delete(data_structure_object, request.user)

            # Return response
            return Response(status=status.HTTP_204_NO_CONTENT)
        except AccessControlError as access_control_exception:
            content = {"message": str(access_control_exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except Http404:
            content = {"message": "Data structure not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, pk):
        """Update a  Curate Data Structure

         Parameters:

            {
                "name": "new_name",
                "form_string": "<new_xml></new_xml>"
                "data": "[data_id]",
                "data_structure_element_root": "[data_structure_element_root_id]"
            }

        Args:

            request: HTTP request
            pk: ObjectId

        Returns:

            - code: 200
              content: Updated  data structure
            - code: 400
              content: Validation error
            - code: 404
              content: Object was not found
            - code: 500
              content: Internal server error
        """
        try:
            # Get object
            data_structure_object = self.get_object(request, pk)

            # Build serializer
            serializer = self.serializer(
                instance=data_structure_object,
                data=request.data,
                partial=True,
                context={"request": request},
            )

            # Validate data
            serializer.is_valid(True)
            # Save data
            serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        except AccessControlError as access_control_exception:
            content = {"message": str(access_control_exception)}
            return Response(content, status=status.HTTP_403_FORBIDDEN)
        except ValidationError as validation_exception:
            content = {"message": validation_exception.detail}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        except Http404:
            content = {"message": "Data structure not found."}
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        except Exception as api_exception:
            content = {"message": str(api_exception)}
            return Response(content, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
