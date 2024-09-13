from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from .models import User

class UserTests(APITestCase):

    def setUp(self):
        self.client = APIClient()

        # Create test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='testuser@example.com',
            age=30,
            gender='male',
            location='Test City',
            income=50000,
            avatar='ShadowClaw'
        )

        # Create another user for testing retrieval
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='testpassword2',
            email='testuser2@example.com',
            age=25,
            gender='female',
            location='Another City',
            income=45000,
            avatar='Thunderwing'
        )

        # URL endpoints
        self.user_list_url = reverse('user-list')  # Adjust if necessary
        self.user_detail_url = reverse('user-detail', args=[self.user.user_id])  # Updated field name
        self.register_url = reverse('register')

    def test_get_all_users(self):
        response = self.client.get(self.user_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Two users are created

    def test_get_user_detail(self):
        response = self.client.get(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_get_user_detail_nonexistent(self):
        nonexistent_user_url = reverse('user-detail', args=[9999])
        response = self.client.get(nonexistent_user_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_register_new_user(self):
        data = {
            "username": "newuser",
            "password": "newpassword123",
            "email": "newuser@example.com",
            "age": 28,
            "gender": "female",
            "location": "Test City",
            "income": 60000,
            "avatar": "AuroraBreath"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)  # Two existing users plus the new one

    def test_register_new_user_invalid(self):
        data = {
            "username": "",  # Invalid empty username
            "password": "newpassword123",
            "email": "newuser@example.com",
            "age": 28,
            "gender": "female",
            "location": "Test City",
            "income": 60000,
            "avatar": "AuroraBreath"
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_patch_user_password(self):
        data = {
            "old_password": "testpassword",
            "new_password": "newsecurepassword"
        }
        response = self.client.patch(self.user_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newsecurepassword"))

    def test_patch_user_password_invalid_old(self):
        data = {
            "old_password": "wrongpassword",
            "new_password": "newsecurepassword"
        }
        response = self.client.patch(self.user_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Old password is incorrect", response.data['error'])

    def test_soft_delete_user(self):
        response = self.client.delete(self.user_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_soft_delete_nonexistent_user(self):
        nonexistent_user_url = reverse('user-detail', args=[9999])
        response = self.client.delete(nonexistent_user_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
