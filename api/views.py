from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from market.models import Market
from investment_simulation.models import InvestmentSimulation
from assessment.models import Assessment
from quizzes.models import Quiz
from quiz_results.models import QuizResult
from virtualmoney.models import VirtualMoney
from .serializers import VirtualMoneySerializer
from achievements.models import Achievement
from .serializers import (
    MarketSerializer,
    InvestmentSimulationSerializer,
    AssessmentSerializer,
    QuizSerializer,
    QuizResultSerializer,
    UserSerializer,
    AchievementSerializer,
    RegisterSerializer,
)
import logging
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

logger = logging.getLogger(__name__)
User = get_user_model()

"""
Filter classes for dashboard metrics
"""
class UserFilter(filters.FilterSet):
    username = filters.CharFilter(field_name='username', lookup_expr='icontains')
    is_active = filters.BooleanFilter(field_name='is_active')

    class Meta:
        model = User
        fields = ['username', 'is_active']

class MarketFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Market
        fields = ['name', 'is_active']

class InvestmentSimulationFilter(filters.FilterSet):
    risk_level = filters.RangeFilter(field_name='risk_level')
    investment_type = filters.CharFilter(field_name='investment_type', lookup_expr='icontains')
    user = filters.CharFilter(field_name='user__username', lookup_expr='icontains')

    class Meta:
        model = InvestmentSimulation
        fields = ['risk_level', 'investment_type', 'user', 'is_active']

class QuizResultFilter(filters.FilterSet):
    score = filters.RangeFilter(field_name='score')
    user = filters.CharFilter(field_name='user__username', lookup_expr='icontains')

    class Meta:
        model = QuizResult
        fields = ['score', 'user', 'is_active']

"""
MarketListView:
   - Handles list operations for the `Market` model, including:
     - GET: Retrieves all active market entries.
     - POST: Creates a new market entry.
"""
class MarketListView(APIView):
   filter_backends = [DjangoFilterBackend]
   filterset_class = MarketFilter  # Adding filter

   def get(self, request):
       logger.info("Fetching all active markets")
       markets = Market.objects.filter(is_active=True)
       filtered_markets = self.filterset_class(request.GET, queryset=markets)  # Applying filter
       serializer = MarketSerializer(filtered_markets.qs, many=True)
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
    filter_backends = [DjangoFilterBackend]
    filterset_class = InvestmentSimulationFilter  # Adding filter

    def get(self, request):
        logger.info("Fetching all investment simulations")
        simulations = InvestmentSimulation.objects.filter(is_active=True)
        filtered_simulations = self.filterset_class(request.GET, queryset=simulations)  # Applying filter
        serializer = InvestmentSimulationSerializer(filtered_simulations.qs, many=True)
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

class InvestmentSimulationDetailView(APIView):
    def get(self, request, id):
        try:
            logger.info(f"Fetching investment simulation with ID: {id}")
            simulation = InvestmentSimulation.objects.get(id=id, is_active=True)
            serializer = InvestmentSimulationSerializer(simulation)
            return Response(serializer.data)
        except InvestmentSimulation.DoesNotExist:
            logger.error(f"Investment simulation with ID {id} not found")
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        try:
            logger.info(f"Updating investment simulation with ID: {id}")
            simulation = InvestmentSimulation.objects.get(id=id, is_active=True)
            serializer = InvestmentSimulationSerializer(simulation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Investment simulation with ID {id} updated successfully")
                return Response(serializer.data)
            logger.error(f"Investment simulation update failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except InvestmentSimulation.DoesNotExist:
            logger.error(f"Investment simulation with ID {id} not found")
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        try:
            logger.info(f"Attempting to soft delete investment simulation with ID: {id}")
            simulation = InvestmentSimulation.objects.get(id=id, is_active=True)
            simulation.is_active = False
            simulation.save()
            logger.info(f"Investment simulation with ID {id} soft deleted successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvestmentSimulation.DoesNotExist:
            logger.error(f"Investment simulation with ID {id} not found")
            return Response(status=status.HTTP_404_NOT_FOUND)

"""
Handles creating and retrieving quizzes
"""
class QuizView(APIView):
    """
    Create a new quiz or retrieve all active quizzes.
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

    def get(self, request):
        logger.info("Retrieving all active quizzes")
        quizzes = Quiz.objects.filter(is_active=True)
        serializer = QuizSerializer(quizzes, many=True)
        logger.info(f"{len(quizzes)} active quizzes retrieved")
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class QuizDetailView(APIView):
    """
    Retrieve, update, or soft delete a specific quiz by ID.
    """
    def get(self, request, id):
        logger.info(f"Received request to fetch quiz with quiz_id: {id}")
        try:
            quiz = Quiz.objects.get(id=id, is_active=True)
            serializer = QuizSerializer(quiz)
            logger.info(f"Successfully fetched quiz: {id}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Quiz.DoesNotExist:
            logger.warning(f"Quiz with quiz_id {id} not found or inactive")
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Internal server error when fetching quiz {id}: {str(e)}")
            return Response({"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, id):
        logger.info(f"Updating quiz with ID {id}")
        try:
            quiz = Quiz.objects.get(id=id, is_active=True)
            serializer = QuizSerializer(quiz, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Quiz {id} updated")
                return Response(serializer.data)
            logger.error(f"Invalid data for quiz {id}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Quiz.DoesNotExist:
            logger.error(f"Quiz {id} not found")
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        logger.info(f"Soft deleting quiz with ID {id}")
        try:
            quiz = Quiz.objects.get(id=id, is_active=True)
            quiz.soft_delete()  # Ensure your model has a soft_delete method
            logger.info(f"Quiz {id} soft deleted")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Quiz.DoesNotExist:
            logger.error(f"Quiz {id} not found")
            return Response({"error": "Quiz not found"}, status=status.HTTP_404_NOT_FOUND)


class QuizResultView(APIView):
   filter_backends = [DjangoFilterBackend]
   filterset_class = QuizResultFilter  # Adding filter

   def post(self, request):
       logger.info("Creating a new quiz result")
       serializer = QuizResultSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           logger.info("Quiz result created")
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       logger.error("Invalid quiz result data")
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   def get(self, request):
       logger.info("Retrieving all active quiz results")
       quiz_results = QuizResult.objects.filter(is_active=True)
       filtered_quiz_results = self.filterset_class(request.GET, queryset=quiz_results)  # Applying filter
       serializer = QuizResultSerializer(filtered_quiz_results.qs, many=True)
       logger.info(f"{len(quiz_results)} active quiz results retrieved")
       return Response(serializer.data)

class QuizResultDetailView(APIView):
   """
   Retrieve a specific quiz result by ID
   """
   def get(self, request, id):
       logger.info(f"Retrieving quiz result with ID {id}")
       try:
           quiz_result = QuizResult.objects.get(id=id, is_active=True)
           serializer = QuizResultSerializer(quiz_result)
           logger.info(f"Quiz result {id} retrieved")
           return Response(serializer.data, status=status.HTTP_200_OK)
       except QuizResult.DoesNotExist:
           logger.error(f"Quiz result {id} not found")
           return Response({"error": "Quiz result not found"}, status=status.HTTP_404_NOT_FOUND)
   """
   Update a specific quiz result by ID
   """
   def put(self, request, id):
       logger.info(f"Updating quiz result with ID {id}")
       try:
           quiz_result = QuizResult.objects.get(id=id, is_active=True)
           serializer = QuizResultSerializer(quiz_result, data=request.data)
           if serializer.is_valid():
               serializer.save()
               logger.info(f"Quiz result {id} updated")
               return Response(serializer.data, status=status.HTTP_200_OK)
           logger.error(f"Invalid data for quiz result {id}")
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       except QuizResult.DoesNotExist:
           logger.error(f"Quiz result {id} not found")
           return Response({"error": "Quiz result not found"}, status=status.HTTP_404_NOT_FOUND)
   """
   Soft delete a specific quiz result by ID using the soft_delete() method
   """
   def delete(self, request, id):
       logger.info(f"Soft deleting quiz result with ID {id}")
       try:
           quiz_result = QuizResult.objects.get(id=id, is_active=True)
           quiz_result.soft_delete()
           logger.info(f"Quiz result {id} soft deleted")
           return Response(status=status.HTTP_204_NO_CONTENT)
       except QuizResult.DoesNotExist:
           logger.error(f"Quiz result {id} not found")
           return Response({"error": "Quiz result not found"}, status=status.HTTP_404_NOT_FOUND)

"""
UserListView:
   - Handles listing all users with filter capabilities for username and active status.
"""
class UserListView(APIView):
   filter_backends = [DjangoFilterBackend]
   filterset_class = UserFilter  # Adding filter

   def get(self, request):
       users = User.objects.all()
       filtered_users = self.filterset_class(request.GET, queryset=users)  # Applying filter
       serializer = UserSerializer(filtered_users.qs, many=True)
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
           user = User.objects.get(user_id=id)
           serializer = UserSerializer(user)
           logger.info(f"Retrieved details for user {user.username}.")
           return Response(serializer.data, status=status.HTTP_200_OK)
       except User.DoesNotExist:
           logger.error(f"User with ID {id} not found.")
           return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
   def patch(self, request, id):
        try:
            user = User.objects.get(user_id=id)
            data = request.data.copy()

            # Check if the old and new passwords are provided in the request
            old_password = data.get('old_password', None)
            new_password = data.get('new_password', None)

            # If both passwords are provided, verify the old password and update to the new one
            if old_password and new_password:
                # Check if the old password matches the current one
                if not user.check_password(old_password):
                    logger.warning(f"Failed to update password for user {user.username}: old password mismatch.")
                    return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

                # Set the new password and hash it
                user.set_password(new_password)
                user.save()
                logger.info(f"Password for user {user.username} updated successfully.")

                # Remove the password fields from the data to avoid saving them in plaintext
                data.pop('old_password')
                data.pop('new_password')

            # Perform the partial update for the remaining fields
            serializer = UserSerializer(user, data=data, partial=True)
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
           user = User.objects.get(user_id=id)
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
   def post(self, request, *args, **kwargs):
       serializer = RegisterSerializer(data=request.data)
       if serializer.is_valid():
           user = serializer.save()
           logger.info(f"User {user.email} registered successfully.")
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       logger.error(f"Registration failed: {serializer.errors}")
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
AssessmentListView:
   - Handles listing and creation of assessments with the ability to filter.
"""
class AssessmentListView(APIView):
   filter_backends = [DjangoFilterBackend]
   filterset_class = filters.FilterSet  # No custom filter added for simplicity

   def get(self, request):
       assessments = Assessment.objects.filter(is_active=True)
       filtered_assessments = self.filterset_class(request.GET, queryset=assessments)  # Applying filter
       serializer = AssessmentSerializer(filtered_assessments.qs, many=True)
       logger.info("Listed all active Assessments")
       return Response(serializer.data)

   def post(self, request):
       serializer = AssessmentSerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           logger.info("Created a new Assessment")
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       else:
           logger.error("Failed to create a new Assessment: %s", serializer.errors)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
      
class VirtualMoneyView(APIView):
   """
   Handles creating and listing VirtualMoney instances.
   """
   def post(self, request):
       """
       Create a new VirtualMoney instance.
       """
       logger.info('POST request received for VirtualMoney')
       serializer = VirtualMoneySerializer(data=request.data)
       if serializer.is_valid():
           serializer.save()
           logger.info('VirtualMoney created successfully')
           return Response(serializer.data, status=status.HTTP_201_CREATED)
       logger.error('Validation errors: %s', serializer.errors)
       return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   """
   List all VirtualMoney instances.
   """
   def get(self, request):
       """
       Retrieve a list of all VirtualMoney instances.
       """
       logger.info('GET request received for VirtualMoney list')
       virtual_moneys = VirtualMoney.objects.all()
       serializer = VirtualMoneySerializer(virtual_moneys, many=True)
       return Response(serializer.data)
class VirtualMoneyDetailView(APIView):
   def get(self, request, id):
       try:
           virtual_money = VirtualMoney.objects.get(id=id)
           serializer = VirtualMoneySerializer(virtual_money)
           return Response(serializer.data)
       except VirtualMoney.DoesNotExist:
           return Response({"error": "Virtual Money not found"}, status=status.HTTP_404_NOT_FOUND)
   def patch(self, request, id):
       try:
           virtual_money = VirtualMoney.objects.get(id= id)
           serializer = VirtualMoneySerializer(virtual_money, data=request.data, partial=True)
           if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       except VirtualMoney.DoesNotExist:
           return Response({"error": "Virtual Money not found"}, status=status.HTTP_404_NOT_FOUND)


       except VirtualMoney.DoesNotExist:
           return Response({"error": "VirtualMoney not found"}, status=status.HTTP_404_NOT_FOUND)
   def delete(self, request, id):
       try:
           virtual_money = VirtualMoney.objects.get(id=id)
           virtual_money.is_active = False
           virtual_money.save()
           return Response(status=status.HTTP_204_NO_CONTENT)
       except VirtualMoney.DoesNotExist:
           return Response({"error": "VirtualMoney not found"}, status=status.HTTP_404_NOT_FOUND)
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


   def get(self, request,id ):
       """
       Retrieve a specific Achievement instance by ID.
       """
       try:
           achievement = Achievement.objects.get(id=id)
           serializer = AchievementSerializer(achievement)
           return Response(serializer.data)
       except Achievement.DoesNotExist:
           return Response({"error": "Achievement not found"}, status=status.HTTP_404_NOT_FOUND)


   """
   Update a specific Achievement instance by ID.
   """
   def patch(self, request,id ):
       """
       Partially update a specific Achievement instance by ID.
       """
       try:
           achievement = Achievement.objects.get(id=id)
           serializer = AchievementSerializer(achievement, data=request.data, partial=True)
           if serializer.is_valid():
               serializer.save()
               return Response(serializer.data)
           return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       except Achievement.DoesNotExist:
           return Response({"error": "Achievement not found"}, status=status.HTTP_404_NOT_FOUND)



