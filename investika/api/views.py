import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from assessment.models import Assessment
from .serializers import AssessmentSerializer

# Set up a logger for this module
logger = logging.getLogger(__name__)

class AssessmentDetailView(APIView):
    """
    Retrieve, update, or soft delete a specific Assessment instance based on its ID.
    """
    
    def get(self, request, assessment_id):
        """
        Retrieve a specific Assessment by its ID.

        Returns:
            Response: The HTTP response containing the Assessment data or 404 status if not found.
        """
        try:
            assessment = Assessment.objects.get(assessment_id=assessment_id)
            serializer = AssessmentSerializer(assessment)
            logger.info(f"Retrieved Assessment with ID {assessment_id}")
            return Response(serializer.data)
        except Assessment.DoesNotExist:
            logger.error(f"Assessment with ID {assessment_id} not found")
            return Response({'detail': 'Assessment not found.'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, assessment_id):
        """
        Update a specific Assessment by its ID.

        Returns:
            Response: The HTTP response with the updated Assessment data or 400 status if validation fails.
        """
        try:
            assessment = Assessment.objects.get(assessment_id=assessment_id)
            serializer = AssessmentSerializer(assessment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Updated Assessment with ID {assessment_id}")
                return Response(serializer.data)
            else:
                logger.error(f"Failed to update Assessment with ID {assessment_id}: %s", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Assessment.DoesNotExist:
            logger.error(f"Assessment with ID {assessment_id} not found for update")
            return Response({'detail': 'Assessment not found.'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, assessment_id):
        """
        Soft delete a specific Assessment by its ID by marking it as inactive.

        Returns:
            Response: The HTTP response with a 204 status if the soft deletion was successful or 404 status if not found.
        """
        try:
            assessment = Assessment.objects.get(assessment_id=assessment_id)
            assessment.is_active = False  # Soft delete by marking as inactive
            assessment.save()
            logger.info(f"Soft deleted Assessment with ID {assessment_id}")
            return Response({'detail': 'Assessment soft deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        except Assessment.DoesNotExist:
            logger.error(f"Assessment with ID {assessment_id} not found for soft deletion")
            return Response({'detail': 'Assessment not found.'}, status=status.HTTP_404_NOT_FOUND)

class AssessmentListView(APIView):
    """
    List all Assessments or create a new Assessment.
    """
    
    def get(self, request):
        """
        List all Assessments.

        Returns:
            Response: The HTTP response containing a list of all Assessments.
        """
        assessments = Assessment.objects.filter(is_active=True)
        serializer = AssessmentSerializer(assessments, many=True)
        logger.info("Listed all active Assessments")
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new Assessment.

        Returns:
            Response: The HTTP response with the created Assessment data or 400 status if validation fails.
        """
        serializer = AssessmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Created a new Assessment")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error("Failed to create a new Assessment: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
