from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.utils import timezone
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
            spending_on_wants=Decimal('100.00'),
            spending_on_needs=Decimal('200.00'),
            savings=Decimal('300.00'),
            investment=Decimal('400.00'),
            is_active=True
        )

        # URL endpoints
        self.assessment_list_url = reverse('assessment-list')
        self.assessment_detail_url = reverse('assessment-detail', args=[self.assessment.assessment_id])

    def test_create_assessment(self):
        """
        Test happy path for creating an Assessment.
        """
        data = {
            "user_id": self.user.user_id,
            "spending_on_wants": "150.00",
            "spending_on_needs": "250.00",
            "savings": "350.00",
            "investment": "450.00",
        }
        response = self.client.post(self.assessment_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Assessment.objects.count(), 2)  # 1 from setUp and 1 new

    def test_create_assessment_invalid_data(self):
        """
        Test unhappy path for creating an Assessment with invalid data.
        """
        data = {
            "user_id": None,  # Missing user
            "spending_on_wants": "invalid",  # Invalid value for DecimalField
            "spending_on_needs": "-100.00",  # Negative value might be invalid depending on validation
            "savings": "100.00",
            "investment": "400.00",
        }
        response = self.client.post(self.assessment_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_assessment_list(self):
        """
        Test happy path for retrieving the list of Assessments.
        """
        response = self.client.get(self.assessment_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # 1 active assessment from setUp

    def test_get_assessment_detail(self):
        """
        Test happy path for retrieving a specific Assessment.
        """
        response = self.client.get(self.assessment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['assessment_id'], self.assessment.assessment_id)

    def test_get_nonexistent_assessment(self):
        """
        Test unhappy path for retrieving a non-existent Assessment.
        """
        non_existent_id = 9999
        response = self.client.get(reverse('assessment-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_assessment(self):
        """
        Test happy path for updating an Assessment.
        """
        data = {"spending_on_wants": "180.00"}
        response = self.client.put(self.assessment_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assessment.refresh_from_db()
        self.assertEqual(self.assessment.spending_on_wants, Decimal('180.00'))

    def test_update_invalid_assessment(self):
        """
        Test unhappy path for updating an Assessment with invalid data.
        """
        data = {"spending_on_wants": "invalid"}  # Invalid data for DecimalField
        response = self.client.put(self.assessment_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_soft_delete_assessment(self):
        """
        Test happy path for soft deleting an Assessment (marking it as inactive).
        """
        response = self.client.delete(self.assessment_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assessment.refresh_from_db()
        self.assertFalse(self.assessment.is_active)  # Check soft delete

    def test_delete_nonexistent_assessment(self):
        """
        Test unhappy path for soft deleting a non-existent Assessment.
        """
        non_existent_id = 9999
        response = self.client.delete(reverse('assessment-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



