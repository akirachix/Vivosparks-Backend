from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from market.models import Market

class MarketTests(APITestCase):

    def setUp(self):
        # Set up test client and initial test data
        self.client = APIClient()
        self.market = Market.objects.create(
            market_name="Stocks",
            risk_level="High",
            description="High-risk stock market",
            is_active=True
        )
        
        # URLs for list and detail views
        self.market_list_url = reverse('market-list')
        self.market_detail_url = reverse('market-detail', args=[self.market.market_id])

    def test_create_market(self):
        """
        Test happy path for creating a new market.
        """
        data = {
            "market_name": "Crypto",
            "risk_level": "Extreme",
            "description": "Highly volatile cryptocurrency market",
            "is_active": True
        }
        response = self.client.post(self.market_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Market.objects.count(), 2)

    def test_create_market_invalid(self):
        """
        Test unhappy path for creating a new market with invalid data.
        """
        data = {
            "market_name": "",
            "risk_level": "Extreme",
            "description": "",  # Missing essential fields
        }
        response = self.client.post(self.market_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_market_list(self):
        """
        Test happy path for getting the list of active markets.
        """
        response = self.client.get(self.market_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only 1 active market exists

    def test_get_market_detail(self):
        """
        Test happy path for retrieving a single market by its ID.
        """
        response = self.client.get(self.market_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['market_id'], self.market.market_id)

    def test_get_market_detail_nonexistent(self):
        """
        Test unhappy path for retrieving a non-existent or inactive market.
        """
        non_existent_id = 9999
        response = self.client.get(reverse('market-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_market(self):
        """
        Test happy path for updating an existing market.
        """
        data = {
            "market_name": "Updated Market",
            "risk_level": "Medium",
            "description": "Updated description",
        }
        response = self.client.put(self.market_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.market.refresh_from_db()
        self.assertEqual(self.market.market_name, "Updated Market")
        self.assertEqual(self.market.risk_level, "Medium")

    def test_update_market_invalid(self):
        """
        Test unhappy path for updating a market with invalid data.
        """
        data = {
            "market_name": "",  # Invalid name
            "risk_level": "Low",
            "description": "Updated description",
        }
        response = self.client.put(self.market_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_soft_delete_market(self):
        """
        Test happy path for soft deleting (deactivating) a market.
        """
        response = self.client.delete(self.market_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.market.refresh_from_db()
        self.assertFalse(self.market.is_active)  # Market should be inactive

    def test_soft_delete_nonexistent_market(self):
        """
        Test unhappy path for attempting to soft delete a non-existent market.
        """
        non_existent_id = 9999
        response = self.client.delete(reverse('market-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


