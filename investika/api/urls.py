from django.urls import path
from .views import AchievementView, AchievementDetailView

urlpatterns = [
    # List all achievements
    path('achievements/', AchievementView.as_view(), name='achievement-list'),
    path('achievements/<int:id>/', AchievementDetailView.as_view(), name='achievement-detail'),
   
    
]

