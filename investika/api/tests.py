from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from market.models import Market
from investment_simulation.models import InvestmentSimulation
from quizzes.models import Quiz
from quiz_results.models import QuizResult
from assessment.models import Assessment
from django.contrib.auth.models import User
from virtualmoney.models import VirtualMoney
from achievements.models import Achievement
from users.models import User
from .serializers import (
    MarketSerializer,
    InvestmentSimulationSerializer,
    QuizSerializer,
    QuizResultSerializer,
    AssessmentSerializer,
    UserSerializer,
    RegisterSerializer,
    VirtualMoneySerializer,
    AchievementSerializer
)
   
def test_put_market_bad_request(self):
    """Test PUTTING invalid data to update a market (bad request)."""
    # First, create a valid market instance
    market = Market.objects.create(
        market_name='Market 1',
        risk_level='High',
        description='Valid market',
        is_active=True
    )
    
    bad_market_data = {
        'market_name': '',  # Invalid because market_name cannot be empty
        'risk_level': '',   # Invalid because risk_level cannot be empty
        'description': 'Updated description'
    }
    
    response = self.client.put(reverse('market-detail', args=[market.market_id]), bad_market_data, format='json')
    self.assertEqual(response.status_code, 400)  # Bad request
    self.assertIn('market_name', response.data)  # Ensure 'market_name' is mentioned in errors
    self.assertIn('risk_level', response.data)   # Ensure 'risk_level' is mentioned in errors
    
def test_put_market_bad_request(self):
    """Test PUTTINGing invalid data to update a market (bad request)."""
    # First, create a valid market instance
    market = Market.objects.create(
        market_name='Market 1',
        risk_level='High',
        description='Valid market',
        is_active=True
    )
    
    bad_market_data = {
        'market_name': '',  # Invalid because market_name cannot be empty
    }
    
    response = self.client.patch(reverse('market-detail', args=[market.market_id]), bad_market_data, format='json')
    self.assertEqual(response.status_code, 400)  # Bad request
    self.assertIn('market_name', response.data)  # Ensure 'market_name' is mentioned in errors
    
def test_delete_nonexistent_market(self):
    """Test DELETE on a non-existent market (bad request or not found)."""
    response = self.client.delete(reverse('market-detail', args=[9999]))  # Non-existent ID
    self.assertEqual(response.status_code, 404)  # Not found
    
def test_get_nonexistent_investment_simulation(self):
    """Test GET on a non-existent investment simulation (not found)."""
    response = self.client.get(reverse('investment-simulation-detail', args=[9999]))  # Non-existent ID
    self.assertEqual(response.status_code, 404)  # Not found

    
def test_put_investment_simulation_bad_request(self):
    """Test PUTting invalid data to update an investment simulation (bad request)."""
    # Create a valid investment simulation instance
    market = Market.objects.create(market_name="Test Market", risk_level="High", description="Market description")
    simulation = InvestmentSimulation.objects.create(market_id=market, amount_invested=1000, outcome='profit', profit_loss=200)
    
    bad_investment_data = {
        'market_id': market.market_id,
        'amount_invested': '',  # Invalid amount_invested (empty)
        'outcome': 'loss'
    }
    response = self.client.put(reverse('investment-simulation-detail', args=[simulation.simulation_id]), bad_investment_data, format='json')
    self.assertEqual(response.status_code, 400)  # Bad request
    self.assertIn('amount_invested', response.data)  # Ensure 'amount_invested' is in the errors
    
def test_get_nonexistent_market(self):
    """Test GET on a non-existent market (not found)."""
    response = self.client.get(reverse('market-detail', args=[9999]))  # Non-existent ID
    self.assertEqual(response.status_code, 404)  # Not found

    
def test_patch_investment_simulation_bad_request(self):
    """Test PATCHing invalid data to update an investment simulation (bad request)."""
    # Create a valid investment simulation instance
    market = Market.objects.create(market_name="Test Market", risk_level="High", description="Market description")
    simulation = InvestmentSimulation.objects.create(market_id=market, amount_invested=1000, outcome='profit', profit_loss=200)
    
    bad_investment_data = {
        'amount_invested': ''  # Invalid amount_invested (empty)
    }
    response = self.client.patch(reverse('investment-simulation-detail', args=[simulation.simulation_id]), bad_investment_data, format='json')
    self.assertEqual(response.status_code, 400)  # Bad request
    self.assertIn('amount_invested', response.data)  # Ensure 'amount_invested' is in the errors
    
def test_delete_nonexistent_investment_simulation(self):
    """Test DELETE on a non-existent investment simulation (not found)."""
    response = self.client.delete(reverse('investment-simulation-detail', args=[9999]))  # Non-existent ID
    self.assertEqual(response.status_code, 404)  # Not found

def test_get_nonexistent_investment_simulation(self):
    """Test GET on a non-existent investment simulation (not found)."""
    response = self.client.get(reverse('investment-simulation-detail', args=[9999]))  # Non-existent ID
    self.assertEqual(response.status_code, 404)  # Not found

def test_patch_investment_simulation_bad_request(self):
    """Test PATCHing invalid data to update an investment simulation (bad request)."""
    # Create a valid investment simulation instance
    market = Market.objects.create(market_name="Test Market", risk_level="High", description="Market description")
    simulation = InvestmentSimulation.objects.create(market_id=market, amount_invested=1000, outcome='profit', profit_loss=200)
    
    bad_investment_data = {
        'amount_invested': ''  # Invalid amount_invested (empty)
    }
    response = self.client.patch(reverse('investment-simulation-detail', args=[simulation.simulation_id]), bad_investment_data, format='json')
    self.assertEqual(response.status_code, 400)  # Bad request
    self.assertIn('amount_invested', response.data)  # Ensure 'amount_invested' is in the errors
    
def test_delete_nonexistent_investment_simulation(self):
    """Test DELETE on a non-existent investment simulation (not found)."""
    response = self.client.delete(reverse('investment-simulation-detail', args=[9999]))  # Non-existent ID
    self.assertEqual(response.status_code, 404)  # Not found

def test_get_nonexistent_investment_simulation(self):
    """Test GET on a non-existent investment simulation (not found)."""
    response = self.client.get(reverse('investment-simulation-detail', args=[9999]))  # Non-existent ID
    self.assertEqual(response.status_code, 404)  # Not found
    
def test_put_quiz_bad_request(self):
    """Test PUTting invalid data to update a quiz (bad request)."""
    quiz = Quiz.objects.create(quiz_text="What is the capital of France?", is_active=True)
    
    bad_quiz_data = {
        'quiz_text': ''  # Invalid because quiz_text cannot be empty
    }
    response = self.client.put(reverse('quiz-detail', args=[quiz.quiz_id]), bad_quiz_data, format='json')
    self.assertEqual(response.status_code, 400)  # Bad request
    self.assertIn('quiz_text', response.data)  # Ensure 'quiz_text' is in the errors
def test_get_valid_virtual_money(self):
        response = self.client.get(reverse('virtualmoney-detail', kwargs={'id': self.virtual_money.id}))
        virtual_money = VirtualMoney.objects.get(id=self.virtual_money.id)
        serializer = VirtualMoneySerializer(virtual_money)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

def test_get_invalid_virtual_money(self):
        response = self.client.get(reverse('virtualmoney-detail', kwargs={'id': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

def test_patch_valid_virtual_money(self):
        response = self.client.patch(reverse('virtualmoney-detail', kwargs={'id': self.virtual_money.id}),
                                     data=self.valid_payload, format='json')
        self.virtual_money.refresh_from_db()
        self.assertEqual(self.virtual_money.balance, 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

def test_patch_invalid_virtual_money(self):
        response = self.client.patch(reverse('virtualmoney-detail', kwargs={'id': self.virtual_money.id}),
                                     data=self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

def test_patch_nonexistent_virtual_money(self):
        response = self.client.patch(reverse('virtualmoney-detail', kwargs={'id': 999}),
                                     data=self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

def test_delete_valid_virtual_money(self):
        response = self.client.delete(reverse('virtualmoney-detail', kwargs={'id': self.virtual_money.id}))
        self.virtual_money.refresh_from_db()
        self.assertFalse(self.virtual_money.is_active)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

def test_delete_nonexistent_virtual_money(self):
        response = self.client.delete(reverse('virtualmoney-detail', kwargs={'id': 999}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        

def test_get_all_users(self):
        response = self.client.get(reverse('user-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)  # We created 3 users in setup

    # Test case for UserDetailView (GET user by id)
def test_get_user_by_id(self):
        response = self.client.get(reverse('user-detail', args=[self.user1.user_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user1.username)

    # Test case for UserDetailView (GET non-existent user)
def test_get_nonexistent_user(self):
        response = self.client.get(reverse('user-detail', args=[9999]))  # Non-existent user ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # Test case for UserDetailView (PUT success)
def test_put_update_user(self):
        updated_data = {
            "username": "updateduser",
            "password": "newpassword123"
        }
        response = self.client.put(reverse('user-detail', args=[self.user1.user_id]), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], updated_data['username'])

    # Test case for UserDetailView (PUT bad request)
def test_put_user_bad_request(self):
        response = self.client.put(reverse('user-detail', args=[self.user1.user_id]), self.invalid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    # Test case for UserDetailView (PATCH success)
def test_patch_update_user(self):
        patch_data = {"username": "patcheduser"}
        response = self.client.patch(reverse('user-detail', args=[self.user1.user_id]), patch_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], patch_data['username'])

    # Test case for UserDetailView (DELETE user)
def test_delete_user(self):
        response = self.client.delete(reverse('user-detail', args=[self.user2.user_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Test case for UserDetailView (DELETE non-existent user)
def test_delete_nonexistent_user(self):
        response = self.client.delete(reverse('user-detail', args=[9999]))  # Non-existent user ID
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
def test_post_achievement_bad_request(self):
        """Test POST with invalid data (missing required fields)."""
        data = {
            "achievement_id": "achv3",
            # Missing 'title' and other required fields
        }
        response = self.client.post(reverse('achievement-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

def test_get_all_achievements(self):
        """Test retrieving a list of all Achievements."""
        response = self.client.get(reverse('achievement-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Since we created one in setUp

def test_get_single_achievement_success(self):
        """Test retrieving a single Achievement by ID."""
        response = self.client.get(reverse('achievement-detail', args=[self.achievement.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.achievement.title)

def test_get_single_achievement_not_found(self):
        """Test retrieving a non-existent Achievement."""
        response = self.client.get(reverse('achievement-detail', args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

def test_patch_achievement_success(self):
        """Test partially updating an Achievement."""
        data = {
            "title": "Updated Title"
        }
        response = self.client.patch(reverse('achievement-detail', args=[self.achievement.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])

def test_patch_achievement_bad_request(self):
        """Test PATCHing with invalid data (e.g., empty title)."""
        data = {
            "title": ""  # Invalid title (empty)
        }
        response = self.client.patch(reverse('achievement-detail', args=[self.achievement.id]), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)

def test_delete_achievement_success(self):
        """Test soft deleting an Achievement."""
        response = self.client.delete(reverse('achievement-detail', args=[self.achievement.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Confirm the achievement is inactive (soft deleted)
        self.achievement.refresh_from_db()
        self.assertFalse(self.achievement.is_active)

def test_delete_achievement_not_found(self):
        """Test deleting a non-existent Achievement."""
        response = self.client.delete(reverse('achievement-detail', args=[9999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)














    
