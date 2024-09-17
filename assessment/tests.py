from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from assessment.models import Assessment
from users.models import User  # Assuming there is a User model in the users app
from decimal import Decimal

class AssessmentTests(APITestCase):

    def setUp(self):
        # Set up test data and APIClient
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)  # Authenticated as test user

        # Create an Assessment for testing retrieval, put, delete
        self.assessment = Assessment.objects.create(
            user_id=self.user,
            question_text="Sample question?",
            question_image=None,
            answers=["Answer 1", "Answer 2"],
            correct_answer="Answer 1",
            is_active=True
        )

        # URL endpoints
        self.assessment_list_url = reverse('assessment-list')
        self.assessment_detail_url = reverse('assessment-detail', args=[self.assessment.assessment_id])

    def test_create_assessment(self):
        """Test happy path for creating an Assessment."""
        data = {
            "user_id": self.user.pk,  # Use pk instead of id
            "question_text": "New Sample Question?",
            "question_image": None,
            "answers": ["Answer 1", "Answer 2", "Answer 3"],
            "correct_answer": "Answer 1"
        }
        response = self.client.post(self.assessment_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assessment.objects.count(), 2)  # 1 from setUp and 1 new

    def test_create_assessment_invalid_data(self):
        """Test unhappy path for creating an Assessment with invalid data."""
        data = {
            "user_id": None,  # Missing user
            "question_text": "",  # Empty question text should be invalid
            "answers": "invalid",  # Invalid value for answers
            "correct_answer": "Answer 1",
        }
        response = self.client.post(self.assessment_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_assessment(self):
        """Test unhappy path for updating an Assessment with invalid data."""
        data = {"question_text": ""}  # Invalid data for required field
        response = self.client.put(self.assessment_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Other tests remain unchanged...

