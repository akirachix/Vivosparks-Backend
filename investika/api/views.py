from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated

from market.models import Market
from investment_simulation.models import InvestmentSimulation
from assessment.models import Assessment
from quizzes.models import Quiz
from quiz_results.models import QuizResult

from .serializers import (
    MarketSerializer,
    InvestmentSimulationSerializer,
    AssessmentSerializer,
    QuizSerializer,
    QuizResultSerializer,
    UserSerializer
)

import logging

logger = logging.getLogger(__name__)

User = get_user_model()

"""
MarketListView:
    - Handles list operations for the `Market` model, including:
      - GET: Retrieves all active market entries.
      - POST: Creates a new market entry.
"""
class MarketListView(APIView):
   
    def get(self, request):
        logger.info("Fetching all active markets")
        markets = Market.objects.filter(is_active=True)
        serializer = MarketSerializer(markets, many=True)
        return Response(serializer.data)

  
    def post(self, request):
        logger.info("Creating a new market entry")
        serializer = MarketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Market entry created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Market creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
MarketDetailView:
    - Handles detailed operations on a single market entry, including:
      - GET: Retrieves a single market entry by its ID.
      - PUT: Updates an existing market entry.
      - DELETE: Soft deletes a market entry by marking it as inactive (using the `is_active` field).
"""
class MarketDetailView(APIView):

   
    def get(self, request, market_id):
        try:
            logger.info(f"Fetching market with ID: {market_id}")
            market = Market.objects.get(market_id=market_id, is_active=True)
            serializer = MarketSerializer(market)
            return Response(serializer.data)
        except Market.DoesNotExist:
            logger.error(f"Market with ID {market_id} not found or inactive")
            return Response(status=status.HTTP_404_NOT_FOUND)

 
    def put(self, request, market_id):
        try:
            logger.info(f"Updating market with ID: {market_id}")
            market = Market.objects.get(market_id = market_id, is_active=True)
            serializer = MarketSerializer(market, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Market with ID {market_id} updated successfully")
                return Response(serializer.data)
            logger.error(f"Market update failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Market.DoesNotExist:
            logger.error(f"Market with ID {market_id} not found or inactive")
            return Response(status=status.HTTP_404_NOT_FOUND)

  
    def delete(self, request, market_id):
        try:
            logger.info(f"Attempting to deactivate (soft delete) market with ID: {market_id}")
            market = Market.objects.get(market_id = market_id, is_active=True)
            market.is_active = False
            market.save()
            logger.info(f"Market with ID {market_id} deactivated successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Market.DoesNotExist:
            logger.error(f"Market with ID {market_id} not found or already deactivated")
            return Response(status=status.HTTP_404_NOT_FOUND)

"""
InvestmentSimulationListView:
    - Handles list operations for the `InvestmentSimulation` model, including:
      - GET: Retrieves all investment simulations.
      - POST: Creates a new investment simulation entry.
"""
class InvestmentSimulationListView(APIView):
 
    def get(self, request):
        logger.info("Fetching all investment simulations")
        simulations = InvestmentSimulation.objects.all()
        serializer = InvestmentSimulationSerializer(simulations, many=True)
        return Response(serializer.data)

    def post(self, request):
        logger.info("Creating a new investment simulation")
        serializer = InvestmentSimulationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Investment simulation created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Investment simulation creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
InvestmentSimulationDetailView:
    - Handles detailed operations on a single investment simulation entry, including:
      - GET: Retrieves a single investment simulation by its ID.
      - PUT: Updates an existing investment simulation entry.
      - DELETE: Soft deletes an investment simulation entry (implementation for actual soft delete needed).
"""
class InvestmentSimulationDetailView(APIView):

    def get(self, request, simulation_id):
        try:
            logger.info(f"Fetching investment simulation with ID: {simulation_id}")
            simulation = InvestmentSimulation.objects.get(simulation_id = simulation_id)
            serializer = InvestmentSimulationSerializer(simulation)
            return Response(serializer.data)
        except InvestmentSimulation.DoesNotExist:
            logger.error(f"Investment simulation with ID {simulation_id} not found")
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, simulation_id):
        try:
            logger.info(f"Updating investment simulation with ID: {simulation_id}")
            simulation = InvestmentSimulation.objects.get(simulation_id=simulation_id)
            serializer = InvestmentSimulationSerializer(simulation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Investment simulation with ID {simulation_id} updated successfully")
                return Response(serializer.data)
            logger.error(f"Investment simulation update failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except InvestmentSimulation.DoesNotExist:
            logger.error(f"Investment simulation with ID {simulation_id} not found")
            return Response(status=status.HTTP_404_NOT_FOUND)

    
    def delete(self, request, simulation_id):
        try:
            logger.info(f"Attempting to soft delete investment simulation with ID: {simulation_id}")
            simulation = InvestmentSimulation.objects.get(simulation_id=simulation_id)
            simulation.is_active = True
            simulation.save()
            logger.info(f"Investment simulation with ID {simulation_id} soft deleted successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvestmentSimulation.DoesNotExist:
            logger.error(f"Investment simulation with ID {simulation_id} not found")
            return Response(status=status.HTTP_404_NOT_FOUND)


"""
Handles creating and retrieving quizzes
"""
class QuizView(APIView):
    """
    Create a new quiz
    """
    def post(self, request):
        logger.info("Creating a new quiz")
        serializer = QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Quiz created")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Invalid quiz data")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Retrieve all quizzes (excluding inactive ones)
    """
    def get(self, request):
        logger.info("Retrieving all active quizzes")
        quizzes = Quiz.objects.filter(is_active=True)
        serializer = QuizSerializer(quizzes, many=True)
        logger.info(f"{len(quizzes)} active quizzes retrieved")
        return Response(serializer.data, status=status.HTTP_200_OK)

"""
Handles retrieving, updating, and soft deleting a specific quiz by ID
"""
class QuizDetailView(APIView):
    """
    Retrieve, update, and soft delete a specific quiz by quiz_id
    """

    def get(self, request, quiz_id):
        logger.info(f"Received request to fetch quiz with quiz_id: {quiz_id}")
        try:
            quiz = Quiz.objects.get(quiz_id=quiz_id, is_active=True)
            serializer = QuizSerializer(quiz)
            logger.info(f"Successfully fetched quiz: {quiz_id}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Quiz.DoesNotExist:
            logger.warning(f"Quiz with quiz_id {quiz_id} not found or inactive")
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Internal server error when fetching quiz {quiz_id}: {str(e)}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, quiz_id):
        logger.info(f"Updating quiz with ID {quiz_id}")
        try:
            quiz = Quiz.objects.get(id=quiz_id, is_active=True)
            serializer = QuizSerializer(quiz, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Quiz {quiz_id} updated")
                return Response(serializer.data)
            logger.error(f"Invalid data for quiz {quiz_id}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Quiz.DoesNotExist:
            logger.error(f"Quiz {quiz_id} not found")
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, quiz_id):
        logger.info(f"Soft deleting quiz with ID {quiz_id}")
        try:
            quiz = Quiz.objects.get(id=quiz_id, is_active=True)
            quiz.soft_delete() 
            logger.info(f"Quiz {quiz_id} soft deleted")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Quiz.DoesNotExist:
            logger.error(f"Quiz {quiz_id} not found")
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)
"""
Handles creating and retrieving quiz results
"""
class QuizResultView(APIView):
    """
    Create a new quiz result
    """
    def post(self, request):
        logger.info("Creating a new quiz result")
        serializer = QuizResultSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Quiz result created")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error("Invalid quiz result data")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    Retrieve all quiz results (excluding soft-deleted ones)
    """
    def get(self, request):
        logger.info("Retrieving all active quiz results")
        quiz_results = QuizResult.objects.filter(is_active=True)
        serializer = QuizResultSerializer(quiz_results, many=True)
        logger.info(f"{len(quiz_results)} active quiz results retrieved")
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizResultDetailView(APIView):
    """
    Retrieve a specific quiz result by ID
    """
    def get(self, request, result_id):
        logger.info(f"Retrieving quiz result with ID {result_id}")
        try:
            quiz_result = QuizResult.objects.get(result_id=result_id, is_active=True)
            serializer = QuizResultSerializer(quiz_result)
            logger.info(f"Quiz result {result_id} retrieved")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except QuizResult.DoesNotExist:
            logger.error(f"Quiz result {result_id} not found")
            return Response({"error": "Quiz result not found"}, status=status.HTTP_404_NOT_FOUND)

    """
    Update a specific quiz result by ID
    """
    def put(self, request, result_id):
        logger.info(f"Updating quiz result with ID {result_id}")
        try:
            quiz_result = QuizResult.objects.get(result_id=result_id, is_active=True)
            serializer = QuizResultSerializer(quiz_result, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Quiz result {result_id} updated")
                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.error(f"Invalid data for quiz result {result_id}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except QuizResult.DoesNotExist:
            logger.error(f"Quiz result {result_id} not found")
            return Response({"error": "Quiz result not found"}, status=status.HTTP_404_NOT_FOUND)

    """
    Soft delete a specific quiz result by ID using the soft_delete() method
    """
    def delete(self, request, result_id):
        logger.info(f"Soft deleting quiz result with ID {result_id}")
        try:
            quiz_result = QuizResult.objects.get(result_id=result_id, is_active=True)
            quiz_result.soft_delete() 
            logger.info(f"Quiz result {result_id} soft deleted")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except QuizResult.DoesNotExist:
            logger.error(f"Quiz result {result_id} not found")
            return Response({"error": "Quiz result not found"}, status=status.HTTP_404_NOT_FOUND)




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



class UserListView(APIView):
    """ 
    This view returns a list of all users in the system. 
    It uses the `UserSerializer` to serialize the user data and logs the retrieval.
    """
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        logger.info("Retrieved user list.")
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    """
    This view handles retrieving, updating, and deleting a specific user by their ID.
    It supports GET, PUT, PATCH, and DELETE operations.
    - GET: Retrieves user details.
    - PUT: Updates all user data.
    - PATCH: Partially updates user data.
    - DELETE: Soft deletes the user by setting their `is_active` field to False.
    """

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            logger.info(f"Retrieved details for user {user.username}.")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            logger.error(f"User with ID {id} not found.")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"User {user.username} updated successfully.")
                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.warning(f"Failed to update user {user.username}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            logger.error(f"User with ID {id} not found.")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"User {user.username} partially updated successfully.")
                return Response(serializer.data, status=status.HTTP_200_OK)
            logger.warning(f"Failed to partially update user {user.username}: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            logger.error(f"User with ID {id} not found.")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.is_active = False
            user.save()
            logger.info(f"User {user.username} soft-deleted successfully.")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            logger.error(f"User with ID {id} not found.")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)


class RegisterView(APIView):
    """
    This view handles the user registration process.
    It validates the provided registration data, creates a new user, and logs the event.
    If registration fails, it logs the error and returns validation errors.
    """
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            logger.info(f"User {user.username} registered successfully.")
            user_serializer = UserSerializer(user)
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        
        logger.warning(f"User registration failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

