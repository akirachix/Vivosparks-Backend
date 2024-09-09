from django.urls import path
from .views import QuizView, QuizDetailView, QuizResultView, QuizResultDetailView
from django.urls import path
from .views import AssessmentDetailView, AssessmentListView
from django.urls import path
from .views import RegisterView, UserListView, UserDetailView

urlpatterns = [
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

