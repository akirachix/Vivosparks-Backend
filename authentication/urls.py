from django.urls import path
from .views import user_login, loginSSO, callback, logout, index


"""
This module defines the URL patterns for the authentication-related views.
- The `index` view is mapped to the root URL ("").
- The `login_view` handles credential-based login via email and password.
- The `sso_login` view redirects the user to the Auth0 authentication page for SSO login.
- The `logout_view` logs the user out of the Django session and redirects them to the Auth0 logout endpoint.
- The `callback` view processes the authentication response from Auth0 and handles user session management.
"""
urlpatterns = [
   path('login/', user_login, name='user_login'),
   path('logout/', logout, name='logout'),
   path('callback/', callback, name='callback'),
   path('sso-login/', loginSSO, name='login_sso'),
   path('', index, name='index'),
]


