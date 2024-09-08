
from django.urls import path
from .views import QuizView, QuizDetailView, QuizResultView, QuizResultDetailView

urlpatterns = [
    # URLs for Quiz operations
    path('quizzes/', QuizView.as_view(), name='quiz-list-create'),
    path('quizzes/<int:quiz_id>/', QuizDetailView.as_view(), name='quiz-detail'),

    # URLs for QuizResult operations
    path('quiz-results/', QuizResultView.as_view(), name='quizresult-list-create'),
    path('quiz-results/<int:result_id>/', QuizResultDetailView.as_view(), name='quizresult-detail'),
]

