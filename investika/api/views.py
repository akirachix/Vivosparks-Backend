from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from users.models import User
from .serializers import UserSerializer
import logging

# Initialize logger
logger = logging.getLogger(__name__)

class UserView(APIView):
    
    # Handle POST request to create a new user
    def post(self, request):
        logger.info('POST request received to create a new user.')
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('New user created successfully.')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.warning('Failed to create user: %s', serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # Handle GET request to retrieve the authenticated user's details
    def get(self, request):
        logger.info('GET request received to retrieve user details.')
        user = request.user
        serializer = UserSerializer(user)
        logger.info('User details retrieved successfully.')
        return Response(serializer.data)
    
    # Create user instance with password handling
    def create(self, validated_data):
        logger.info('Creating a user instance with password handling.')
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
            logger.info('Password set successfully for the user.')
        user.save()
        logger.info('User instance saved successfully.')
        return user

class UserDetailView(APIView):
    
    # Handle GET request to retrieve user by ID
    def get(self, request, id):
        logger.info('GET request received to retrieve user with ID: %s', id)
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        logger.info('User with ID %s retrieved successfully.', id)
        return Response(serializer.data)
    
    # Handle PATCH request to update user details partially
    def patch(self, request, id):
        logger.info('PATCH request received to update user with ID: %s', id)
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info('User with ID %s updated successfully.', id)
            return Response(serializer.data)
        else:
            logger.warning('Failed to update user with ID %s: %s', id, serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Handle DELETE request to delete user by ID
    def delete(self, request, id):
        logger.info('DELETE request received to delete user with ID: %s', id)
        user = User.objects.get(id=id)
        user.delete()
        logger.info('User with ID %s deleted successfully.', id)
        return Response(status=status.HTTP_204_NO_CONTENT)
