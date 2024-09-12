from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from achievements.models import Achievement
from users.models import User  # Assuming there is a User model in the users app
from datetime import date


class AchievementTests(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        # Create a test achievement
        self.achievement = Achievement.objects.create(
            user_id=self.user,
            title="Test Achievement",
            description="Test description",
            criteria="Test criteria",
            reward_type="Badge",
            date_achieved=date(2023, 1, 1)  # Use date object for proper handling
        )

        # Use the new 'id' field instead of 'achievement_id'
        self.achievement_detail_url = reverse('achievement-detail', args=[self.achievement.id])
        self.achievement_list_url = reverse('achievement-list')

    def test_get_achievement_list(self):
        """
        Test happy path for retrieving the list of Achievements.
        """
        response = self.client.get(self.achievement_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Achievement.objects.count())

    def test_get_achievement_detail(self):
        """
        Test happy path for retrieving a specific Achievement.
        """
        response = self.client.get(self.achievement_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.achievement.title)

    def test_get_nonexistent_achievement(self):
        """
        Test unhappy path for retrieving a non-existent Achievement.
        """
        non_existent_id = 9999
        response = self.client.get(reverse('achievement-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_achievement(self):
        """
        Test happy path for partially updating an Achievement.
        """
        data = {"title": "Updated Achievement Title"}
        response = self.client.patch(self.achievement_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.achievement.refresh_from_db()
        self.assertEqual(self.achievement.title, "Updated Achievement Title")

    def test_patch_invalid_achievement(self):
        """
        Test unhappy path for patching an Achievement with invalid data.
        """
        data = {"date_achieved": "invalid-date"}
        response = self.client.patch(self.achievement_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


