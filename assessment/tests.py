from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from assessment.models import Assessment
from django.contrib.auth import get_user_model

User = get_user_model()

class AssessmentTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

        self.assessment = Assessment.objects.create(
            user_id=self.user,
            question_text="Sample question?",
            question_image=None,
            answers=["Answer 1", "Answer 2"],
            is_active=True
        )

        self.assessment_list_url = reverse('assessment-list')
        self.assessment_detail_url = reverse('assessment-detail', args=[self.assessment.assessment_id])

    def test_create_assessment(self):
        data = {
            "user_id": self.user.user_id,  # Correctly use the User instance ID
            "question_text": "New Sample Question?",
            "question_image": None,
            "answers": ["Answer 1", "Answer 2", "Answer 3"]
        }
        response = self.client.post(self.assessment_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assessment.objects.count(), 2)

    def test_create_assessment_invalid_data(self):
        data = {
            "user_id": None,
            "question_text": "",
            "answers": "invalid",
        }
        response = self.client.post(self.assessment_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid_assessment(self):
        data = {"question_text": ""}
        response = self.client.put(self.assessment_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_soft_delete_assessment(self):
        """Test soft deletion of an Assessment."""
        response = self.assessment.soft_delete()  # Directly call the soft_delete method
        self.assertTrue(self.assessment.is_active == False)  # Check if it is marked inactive

    def test_get_assessment(self):
        response = self.client.get(self.assessment_detail_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question_text'], self.assessment.question_text)
