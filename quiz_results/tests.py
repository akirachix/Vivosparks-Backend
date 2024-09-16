from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from .models import Quiz, QuizResult

class QuizResultTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()
        
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a quiz
        self.quiz = Quiz.objects.create(
            quiz_text='Sample quiz text',
            is_active=True
        )

        # Create a quiz result
        self.quiz_result = QuizResult.objects.create(
            user=self.user,  # User instance
            score=85,  # Example score
            quiz=self.quiz,  # Quiz instance
            is_active=True,
            money_earned=50.00  # Provide a value for money_earned
        )
        
        self.quiz_result_list_create_url = reverse('quizresult-list-create')
        self.quiz_result_detail_url = reverse('quizresult-detail', args=[self.quiz_result.id])
    
    def test_create_quiz_result(self):
        response = self.client.post(self.quiz_result_list_create_url, {
            'user': self.user.user_id,  # Use the User instance's id
            'score': 90,
            'quiz': self.quiz.id,  # Use the Quiz instance's id
            'is_active': True,
            'money_earned': 75.00  # Include money_earned in the request
        }, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_create_quiz_result_invalid(self):
        response = self.client.post(self.quiz_result_list_create_url, {
            'user': 999,  # This should be a valid User ID
            'score': 90,
            'quiz': 999,  # This should be a valid Quiz ID
            'is_active': True,
            'money_earned': 75.00
        }, format='json')
        self.assertEqual(response.status_code, 400)  # Expecting a validation error

    def test_get_quiz_result_detail(self):
        response = self.client.get(self.quiz_result_detail_url)
        self.assertEqual(response.status_code, 200)
    
    # Convert both values to floats for comparison
        money_earned_response = float(response.data['money_earned'])
        money_earned_expected = float(self.quiz_result.money_earned)
    
        self.assertEqual(response.data['score'], self.quiz_result.score)
        self.assertEqual(money_earned_response, money_earned_expected)


    def test_get_quiz_result_list(self):
        response = self.client.get(self.quiz_result_list_create_url)
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.data), 0)

    def test_soft_delete_quiz_result(self):
        self.quiz_result.is_active = False
        self.quiz_result.save()
        response = self.client.get(self.quiz_result_detail_url)
        self.assertEqual(response.status_code, 404)  # Assuming 404 for soft-deleted records

    def test_update_quiz_result(self):
        response = self.client.put(self.quiz_result_detail_url, {
            'user': self.user.user_id,  # Use the User instance's id
            'score': 95,
            'quiz': self.quiz.id,  # Use the Quiz instance's id
            'is_active': True,
            'money_earned': 100.00  # Update money_earned
        }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['score'], 95)
        self.assertEqual(response.data['money_earned'], '100.00')

    def test_update_quiz_result_invalid(self):
        response = self.client.put(self.quiz_result_detail_url, {
            'user': 999,  # This should be a valid User ID
            'score': 'invalid',  # Invalid score value
            'quiz': 999,  # This should be a valid Quiz ID
            'is_active': True,
            'money_earned': 'invalid'  # Invalid money_earned value
        }, format='json')
        self.assertEqual(response.status_code, 400)  # Expecting a validation error
