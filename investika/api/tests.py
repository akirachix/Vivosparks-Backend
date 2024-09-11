from django.test import TestCase
from django.urls import reverse
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

class SerializerTestCase(TestCase):
    
    def test_market_serializer_valid(self):
        """Test for valid data in MarketSerializer"""
        market_data = {
            'market_name': 'Test Market',
            'risk_level': 'High',
            'description': 'A high-risk market',
            'is_active': True
        }
        serializer = MarketSerializer(data=market_data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['market_name'], market_data['market_name'])

    def test_market_serializer_invalid(self):
        """Test for invalid data in MarketSerializer"""
        market_data = {
            # Missing required fields
            'is_active': True
        }
        serializer = MarketSerializer(data=market_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('market_name', serializer.errors)

    def test_investment_simulation_serializer_valid(self):
        """Test for valid data in InvestmentSimulationSerializer"""
        # Create a valid Market instance for the foreign key
        market = Market.objects.create(
            market_name='Test Market',
            risk_level='Medium',
            description='A test market',
            is_active=True
        )
        
        investment_data = {
            'title': 'Investment 1',
            'amount_invested': 1000,
            'profit_loss': 100,
            'outcome': 'profit',
            'market_id': market.market_id  # Use the correct foreign key 'market_id'
        }
        serializer = InvestmentSimulationSerializer(data=investment_data)
        self.assertTrue(serializer.is_valid())

    def test_investment_simulation_serializer_invalid(self):
        """Test for invalid data in InvestmentSimulationSerializer"""
        investment_data = {
            'title': 'Investment 1'
        }
        serializer = InvestmentSimulationSerializer(data=investment_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('amount_invested', serializer.errors)

    def test_quiz_serializer_valid(self):
        """Test for valid data in QuizSerializer"""
        quiz_data = {
            'quiz_text': 'What is the capital of France?',
            'is_active': True
        }
        serializer = QuizSerializer(data=quiz_data)
        self.assertTrue(serializer.is_valid())

    def test_quiz_serializer_invalid(self):
        """Test for invalid data in QuizSerializer"""
        quiz_data = {
            'is_active': True
        }
        serializer = QuizSerializer(data=quiz_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('quiz_text', serializer.errors)

    def test_quiz_result_serializer_valid(self):
        """Test for valid data in QuizResultSerializer"""
        quiz = Quiz.objects.create(quiz_text="Sample Quiz", is_active=True)  # Creating a valid quiz instance
        quiz_result_data = {
            'score': 80,
            'quiz': quiz.quiz_id,  # Use 'quiz_id' instead of 'id'
            'money_earned': 100
        }
        serializer = QuizResultSerializer(data=quiz_result_data)
        self.assertTrue(serializer.is_valid())

    def test_quiz_result_serializer_invalid(self):
        """Test for invalid data in QuizResultSerializer"""
        quiz_result_data = {
            'score': -10  # Invalid negative score
        }
        serializer = QuizResultSerializer(data=quiz_result_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('quiz', serializer.errors)

    def test_assessment_serializer_valid(self):
        """Test for valid data in AssessmentSerializer"""
        assessment_data = {
            'assessment_id': '1',
            'spending_on_wants': 200,
            'spending_on_needs': 500,
            'savings': 1000,
            'investment': 200
        }
        serializer = AssessmentSerializer(data=assessment_data)
        self.assertTrue(serializer.is_valid())

    def test_assessment_serializer_invalid(self):
        """Test for invalid data in AssessmentSerializer"""
        assessment_data = {
            'spending_on_wants': 200
        }
        serializer = AssessmentSerializer(data=assessment_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('spending_on_needs', serializer.errors)

    def test_user_serializer_valid(self):
        """Test for valid data in UserSerializer"""
        user = User.objects.create_user(username="testuser", password="testpass")
        serializer = UserSerializer(user)
        self.assertEqual(serializer.data['username'], user.username)

    def test_register_serializer_valid(self):
        """Test for valid registration data in RegisterSerializer"""
        register_data = {
            'username': 'testuser',
            'password': 'testpass',
            'email': 'testuser@example.com'
        }
        serializer = RegisterSerializer(data=register_data)
        self.assertTrue(serializer.is_valid())

    def test_register_serializer_invalid(self):
        """Test for invalid registration data in RegisterSerializer"""
        register_data = {
            'username': 'testuser',
            'password': '',  # Password cannot be empty
        }
        serializer = RegisterSerializer(data=register_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_virtual_money_serializer_valid(self):
        """Test for valid data in VirtualMoneySerializer"""
        virtual_money_data = {
            'amount': 1000
        }
        serializer = VirtualMoneySerializer(data=virtual_money_data)
        self.assertTrue(serializer.is_valid())

    def test_virtual_money_serializer_invalid(self):
        """Test for invalid data in VirtualMoneySerializer"""
        virtual_money_data = {
            'amount': -500  # Invalid negative amount
        }
        serializer = VirtualMoneySerializer(data=virtual_money_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('amount', serializer.errors)

    def test_achievement_serializer_valid(self):
        """Test for valid data in AchievementSerializer"""
        achievement_data = {
            'achievement_id': '1',
            'title': 'Test Achievement',
            'criteria': 'Complete all tasks',
            'date_achieved': '2023-09-10',
            'reward_type': 'badge',
            'description': 'Test description'
        }
        serializer = AchievementSerializer(data=achievement_data)
        self.assertTrue(serializer.is_valid())

    def test_achievement_serializer_invalid(self):
        """Test for invalid data in AchievementSerializer"""
        achievement_data = {
            'title': '',  # Missing title
            'criteria': 'Complete all tasks'
        }
        serializer = AchievementSerializer(data=achievement_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
        
    def test_get_markets(self):
        response = self.client.get(reverse('market-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_market_by_id(self):
        response = self.client.get(reverse('market-detail', args=[self.market.market_id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['market_name'], self.market.market_name)

    # Investment Simulation Tests
    def test_get_investment_simulations(self):
        response = self.client.get(reverse('investment-simulation-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_investment_simulation_by_id(self):
        response = self.client.get(reverse('investment-simulation-detail', args=[self.simulation.simulation_id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['amount_invested'], str(self.simulation.amount_invested))

    # Quiz Tests
    def test_get_quizzes(self):
        response = self.client.get(reverse('quiz-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_quiz_by_id(self):
        response = self.client.get(reverse('quiz-detail', args=[self.quiz.quiz_id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['quiz_text'], self.quiz.quiz_text)

    # QuizResult Tests
    def test_get_quiz_results(self):
        response = self.client.get(reverse('quiz-result-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_quiz_result_by_id(self):
        response = self.client.get(reverse('quiz-result-detail', args=[self.quiz_result.result_id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['score'], self.quiz_result.score)

    # Assessment Tests
    def test_get_assessments(self):
        response = self.client.get(reverse('assessment-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_assessment_by_id(self):
        response = self.client.get(reverse('assessment-detail', args=[self.assessment.assessment_id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['savings'], str(self.assessment.savings))

    # VirtualMoney Tests
    def test_get_virtual_money(self):
        response = self.client.get(reverse('virtual-money-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_virtual_money_by_id(self):
        response = self.client.get(reverse('virtual-money-detail', args=[self.virtual_money.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['amount'], str(self.virtual_money.amount))

    # Achievement Tests
    def test_get_achievements(self):
        response = self.client.get(reverse('achievement-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_achievement_by_id(self):
        response = self.client.get(reverse('achievement-detail', args=[self.achievement.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], self.achievement.title)

