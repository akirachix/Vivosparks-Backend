from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from quizzes.models import Quiz
from quiz_results.models import QuizResult
from .serializers import QuizSerializer, QuizResultSerializer


import logging


"""
Set up logger
"""
logger = logging.getLogger(__name__)

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
