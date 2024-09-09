# api/urls.py

from django.urls import path
from .views import RegisterView, UserListView, UserDetailView, CompleteProfileView

"""
This module defines the URL patterns for user-related API endpoints.
- The `UserListView` is mapped to 'users/' URL, which provides a list of all users.
- The `RegisterView` is mapped to 'register/' URL, which handles user registration.
- The `UserDetailView` is mapped to 'users/<int:id>/' URL, which provides endpoints for retrieving, updating, and deleting individual users by their ID.
- The `CompleteProfileView` is mapped to 'complete-profile/' URL, which handles profile completion after SSO login.
"""

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('complete-profile/', CompleteProfileView.as_view(), name='complete-profile'),
]
