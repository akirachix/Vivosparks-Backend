from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from market.models import Market
from investment_simulation.models import InvestmentSimulation

class InvestmentSimulationTests(APITestCase):

    def setUp(self):
        # Set up test client and initial test data
        self.client = APIClient()

        # Create a market instance
        self.market = Market.objects.create(
            market_name="Stocks",
            risk_level="High",
            description="High-risk stock market",
            is_active=True
        )

        # Create an investment simulation instance
        self.simulation = InvestmentSimulation.objects.create(
            market_id=self.market,
            amount_invested=1000.00,
            outcome="Profit",
            profit_loss=200.00,
        )
        
        # URLs for list and detail views
        self.simulation_list_url = reverse('investment-simulation-list')
        self.simulation_detail_url = reverse('investment-simulation-detail', args=[self.simulation.id])

    def test_create_investment_simulation(self):
        """
        Test happy path for creating a new investment simulation.
        """
        data = {
            "market_id": self.market.market_id,
            "amount_invested": 1500.00,
            "outcome": "Loss",
            "profit_loss": -100.00,
        }
        response = self.client.post(self.simulation_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(InvestmentSimulation.objects.count(), 2)

    def test_create_investment_simulation_invalid(self):
        """
        Test unhappy path for creating a new investment simulation with invalid data.
        """
        data = {
            "market_id": None,  # Missing market
            "amount_invested": "",  # Invalid amount
            "outcome": "Loss",
            "profit_loss": -100.00,
        }
        response = self.client.post(self.simulation_list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_investment_simulation_list(self):
        """
        Test happy path for getting the list of investment simulations.
        """
        response = self.client.get(self.simulation_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only 1 simulation exists

    def test_get_investment_simulation_detail(self):
        """
        Test happy path for retrieving a single investment simulation by its ID.
        """
        response = self.client.get(self.simulation_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.simulation.id)

    def test_get_investment_simulation_detail_nonexistent(self):
        """
        Test unhappy path for retrieving a non-existent investment simulation.
        """
        non_existent_id = 9999
        response = self.client.get(reverse('investment-simulation-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_investment_simulation(self):
        """
        Test happy path for updating an existing investment simulation.
        """
        data = {
            "market_id": self.market.market_id,
            "amount_invested": 1200.00,
            "outcome": "Profit",
            "profit_loss": 150.00,
        }
        response = self.client.put(self.simulation_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.simulation.refresh_from_db()
        self.assertEqual(self.simulation.amount_invested, 1200.00)
        self.assertEqual(self.simulation.profit_loss, 150.00)

    def test_update_investment_simulation_invalid(self):
        """
        Test unhappy path for updating a simulation with invalid data.
        """
        data = {
            "market_id": self.market.market_id,
            "amount_invested": "",  # Invalid amount
            "outcome": "Profit",
            "profit_loss": 150.00,
        }
        response = self.client.put(self.simulation_detail_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_soft_delete_investment_simulation(self):
        """
        Test happy path for soft deleting (deactivating) an investment simulation.
        """
        response = self.client.delete(self.simulation_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.simulation.refresh_from_db()
        self.assertFalse(self.simulation.is_active)

    def test_soft_delete_nonexistent_investment_simulation(self):
        """
        Test unhappy path for attempting to soft delete a non-existent investment simulation.
        """
        non_existent_id = 9999
        response = self.client.delete(reverse('investment-simulation-detail', args=[non_existent_id]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
