from django.urls import path
from .views import (
    MarketListView, MarketDetailView,
    InvestmentSimulationListView, InvestmentSimulationDetailView,
    QuizView, QuizDetailView, QuizResultView, QuizResultDetailView,
    AssessmentDetailView, AssessmentListView,
    RegisterView, UserListView, UserDetailView,
    VirtualMoneyView, VirtualMoneyDetailView,
    AchievementView, AchievementDetailView
)

# URL patterns for the application
urlpatterns = [
    """URLs for market-related views"""
    path('markets/', MarketListView.as_view(), name='market-list'),  """List all markets"""
    path('markets/<int:market_id>/', MarketDetailView.as_view(), name='market-detail'),  """View details of a specific market by ID"""

    """URLs for investment simulation-related views"""
    path('investment-simulations/', InvestmentSimulationListView.as_view(), name='investment-simulation-list'),  """List all investment simulations"""
    path('investment-simulations/<int:simulation_id>/', InvestmentSimulationDetailView.as_view(), name='investment-simulation-detail'),  """View details of a specific simulation by ID"""

    """URLs for quiz-related views"""
    path('quizzes/', QuizView.as_view(), name='quiz-list-create'),  """List all quizzes and create a new quiz"""
    path('quizzes/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz-detail'),  """View details of a specific quiz by ID"""

    """URLs for quiz result-related views"""
    path('quiz-results/', QuizResultView.as_view(), name='quizresult-list-create'),  """List all quiz results and create a new result"""
    path('quiz-results/<int:result_id>/', QuizResultDetailView.as_view(), name='quizresult-detail'),  """View details of a specific quiz result by ID"""

    """URLs for assessment-related views"""
    path('assessment/', AssessmentListView.as_view(), name='assessment-list'),  """List all assessments"""
    path('assessment/<int:assessment_id>/', AssessmentDetailView.as_view(), name='assessment-detail'),  """View details of a specific assessment by ID"""

    """URL for user registration view"""
    path('register/', RegisterView.as_view(), name='register'),  """User registration page"""

    """URLs for user-related views"""
    path('users/', UserListView.as_view(), name='user-list'),  """List all users"""
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),  """View details of a specific user by ID"""

    """URLs for virtual money-related views"""
    path('virtualmoney/', VirtualMoneyView.as_view(), name='virtualmoney-list'),  """List all virtual money entries"""
    path('virtualmoney/<int:id>/', VirtualMoneyDetailView.as_view(), name='virtualmoney-detail'),  """View details of a specific virtual money entry by ID"""

    """URLs for achievement-related views"""
    path('achievements/', AchievementView.as_view(), name='achievement-list'),  """List all achievements"""
    path('achievements/<int:id>/', AchievementDetailView.as_view(), name='achievement-detail'),  """View details of a specific achievement by ID"""
]
