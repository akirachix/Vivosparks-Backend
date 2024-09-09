from django.urls import path
from .views import AssessmentDetailView, AssessmentListView
from django.urls import path
from .views import RegisterView, UserListView, UserDetailView

urlpatterns = [
    path('assessment/', AssessmentListView.as_view(), name='assessment-list'),
    path('assessment/<int:assessment_id>/', AssessmentDetailView.as_view(), name='assessment-detail'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
]
