from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import VirtualMoney

class VirtualMoneyTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # Fetch the custom user model
        User = get_user_model()

        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create a VirtualMoney instance
        self.virtual_money = VirtualMoney.objects.create(
            user=self.user,  # Use the correct field name
            amount=100.00
        )

        # Define URLs
        self.virtual_money_list_url = reverse('virtualmoney-list')
        self.virtual_money_detail_url = reverse('virtualmoney-detail', args=[self.virtual_money.id])

    def test_create_virtual_money(self):
        """
        Test creating a new VirtualMoney instance (happy path).
        """
        data = {
            "user": self.user.user_id,  # Correct field name
            "amount": 200.00
        }
        response = self.client.post(self.virtual_money_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(VirtualMoney.objects.count(), 2)

    def test_create_virtual_money_invalid(self):
        """
        Test creating a new VirtualMoney instance with invalid data (unhappy path).
        """
        data = {
            "user": "",  # Invalid empty user
            "amount": 200.00
        }
        response = self.client.post(self.virtual_money_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_all_virtual_money(self):
        """
        Test retrieving all active VirtualMoney instances (happy path).
        """
        response = self.client.get(self.virtual_money_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only 1 active instance

    def test_get_virtual_money_detail(self):
        """
        Test retrieving a specific VirtualMoney instance by ID (happy path).
        """
        response = self.client.get(self.virtual_money_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], f"{self.virtual_money.amount:.2f}")


    def test_get_virtual_money_detail_nonexistent(self):
        """
        Test retrieving a non-existent VirtualMoney instance (unhappy path).
        """
        non_existent_id = 9999
        response = self.client.get(reverse('virtualmoney-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_virtual_money(self):
        """
        Test updating an existing VirtualMoney instance (happy path).
        """
        data = {
            "amount": 300.00
        }
        response = self.client.patch(self.virtual_money_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.virtual_money.refresh_from_db()
        self.assertEqual(self.virtual_money.amount, 300.00)

    def test_update_virtual_money_invalid(self):
        """
        Test updating a VirtualMoney instance with invalid data (unhappy path).
        """
        data = {
            "amount": ""  # Invalid empty amount
        }
        response = self.client.patch(self.virtual_money_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_soft_delete_virtual_money(self):
        """
        Test soft deleting a VirtualMoney instance (happy path).
        """
        response = self.client.delete(self.virtual_money_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.virtual_money.refresh_from_db()
        self.assertFalse(self.virtual_money.is_active)  # Check if the instance is marked as inactive

    def test_soft_delete_virtual_money_nonexistent(self):
        """
        Test attempting to soft delete a non-existent VirtualMoney instance (unhappy path).
        """
        non_existent_id = 9999
        response = self.client.delete(reverse('virtualmoney-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
