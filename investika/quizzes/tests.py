from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from .models import Quiz

class QuizTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.quiz = Quiz.objects.create(
            quiz_text="Sample Quiz Text",
            is_active=True
        )
        self.quiz_list_create_url = reverse('quiz-list-create')
        self.quiz_detail_url = reverse('quiz-detail', args=[self.quiz.pk])

    def test_create_quiz(self):
        data = {
            "quiz_text": "New Quiz Text"
        }
        response = self.client.post(self.quiz_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 2)
        self.assertEqual(Quiz.objects.latest('pk').quiz_text, "New Quiz Text")

    def test_create_quiz_invalid(self):
        data = {
            "quiz_text": ""
        }
        response = self.client.post(self.quiz_list_create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_quizzes(self):
        response = self.client.get(self.quiz_list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_quiz_detail(self):
        response = self.client.get(self.quiz_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.quiz.pk)

    def test_get_quiz_detail_nonexistent(self):
        non_existent_id = 9999
        response = self.client.get(reverse('quiz-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_quiz(self):
        data = {
            "quiz_text": "Updated Quiz Text"
        }
        response = self.client.put(self.quiz_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quiz.refresh_from_db()
        self.assertEqual(self.quiz.quiz_text, "Updated Quiz Text")

    def test_update_quiz_invalid(self):
        data = {
            "quiz_text": ""
        }
        response = self.client.put(self.quiz_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_soft_delete_quiz(self):
        response = self.client.delete(self.quiz_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.quiz.refresh_from_db()
        self.assertFalse(self.quiz.is_active)

    def test_soft_delete_nonexistent_quiz(self):
        non_existent_id = 9999
        response = self.client.delete(reverse('quiz-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
