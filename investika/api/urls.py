from django.urls import path
from .views import AssessmentDetailView, AssessmentListView

urlpatterns = [
    path('assessment/', AssessmentListView.as_view(), name='assessment-list'),
    path('assessment/<int:assessment_id>/', AssessmentDetailView.as_view(), name='assessment-detail'),
]
