from django.urls import path
from .views import MarketListView, MarketDetailView
from .views import InvestmentSimulationListView, InvestmentSimulationDetailView
from .views import QuizView, QuizDetailView, QuizResultView, QuizResultDetailView
from .views import AssessmentDetailView, AssessmentListView
from .views import RegisterView, UserListView, UserDetailView

urlpatterns = [
    path('markets/', MarketListView.as_view(), name='market-list'),
    path('markets/<int:market_id>/', MarketDetailView.as_view(), name='market-detail'),
    path('investment-simulations/', InvestmentSimulationListView.as_view(), name='investment-simulation-list'),
    path('investment-simulations/<int:simulation_id>/', InvestmentSimulationDetailView.as_view(), name='investment-simulation-detail'),
    path('quizzes/', QuizView.as_view(), name='quiz-list-create'),
    path('quizzes/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quiz-results/', QuizResultView.as_view(), name='quizresult-list-create'),
    path('quiz-results/<int:result_id>/', QuizResultDetailView.as_view(), name='quizresult-detail'),
    path('assessment/', AssessmentListView.as_view(), name='assessment-list'),
    path('assessment/<int:assessment_id>/', AssessmentDetailView.as_view(), name='assessment-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),

]

