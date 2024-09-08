import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from achievement.models import Achievement
from .serializers import AchievementSerializer

# Set up logging
logger = logging.getLogger(__name__)

class AchievementView(APIView):
    """
    Handles creating and listing Achievement instances.
    """

    def post(self, request):
        """
        Create a new Achievement instance.
        """
        logger.info('POST request received for Achievement')
        serializer = AchievementSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('Achievement created successfully')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error('Validation errors: %s', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    List all Achievement instances.
    """
    def get(self, request):
        """
        Retrieve a list of all Achievement instances.
        """
        logger.info('GET request received for Achievement list')
        achievements = Achievement.objects.all()
        serializer = AchievementSerializer(achievements, many=True)
        return Response(serializer.data)

class AchievementDetailView(APIView):
    """
    Handles retrieval, partial update, and soft deletion of a specific Achievement instance by ID.
    """

    def get(self, request, id):
        """
        Retrieve a specific Achievement instance by ID.
        """
        logger.info('GET request received for Achievement with ID %s', id)
        try:
            achievement = Achievement.objects.get(id=id)
            serializer = AchievementSerializer(achievement)
            return Response(serializer.data)
        except Achievement.DoesNotExist:
            logger.error('Achievement with ID %s not found', id)
            return Response({"error": "Achievement not found"}, status=status.HTTP_404_NOT_FOUND)

    """
    Update a specific Achievement instance by ID.
    """
    def patch(self, request, id):
        """
        Partially update a specific Achievement instance by ID.
        """
        logger.info('PATCH request received for Achievement with ID %s', id)
        try:
            achievement = Achievement.objects.get(id=id)
            serializer = AchievementSerializer(achievement, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info('Achievement updated successfully')
                return Response(serializer.data)
            logger.error('Validation errors: %s', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Achievement.DoesNotExist:
            logger.error('Achievement with ID %s not found', id)
            return Response({"error": "Achievement not found"}, status=status.HTTP_404_NOT_FOUND)

    """
    Soft delete a specific Achievement instance by ID.
    """
    def delete(self, request, id):
        """
        Mark a specific Achievement instance as deleted (soft delete).
        """
        logger.info('DELETE request received for Achievement with ID %s', id)
        try:
            achievement = Achievement.objects.get(id=id)
            achievement.is_active = False  # Mark as deleted
            achievement.save()
            logger.info('Achievement marked as deleted')
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Achievement.DoesNotExist:
            logger.error('Achievement with ID %s not found', id)
            return Response({"error": "Achievement not found"}, status=status.HTTP_404_NOT_FOUND)
        
