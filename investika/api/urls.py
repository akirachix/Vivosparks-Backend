from django.urls import path
from .views import RegisterView, LoginView, LogoutView, ChangePasswordView, UserListView, UserDetailView

urlpatterns = [
    # URL path for user registration
    path('register/', RegisterView.as_view(), name='register'),

    # URL path for user login
    path('login/', LoginView.as_view(), name='login'),

    # URL path for user logout
    path('logout/', LogoutView.as_view(), name='logout'),

    # URL path for changing password
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),

    # URL path for listing all users
    path('users/', UserListView.as_view(), name='user_list'),

    # URL path for user details (with user ID as a dynamic parameter)
    path('users/<int:id>/', UserDetailView.as_view(), name='user_detail'),
]
