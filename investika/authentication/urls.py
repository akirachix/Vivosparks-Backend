from django.urls import path
from . import views

"""
This module defines the URL patterns for the authentication-related views.
- The `index` view is mapped to the root URL ("").
- The `login_view` handles credential-based login via email and password.
- The `sso_login` view redirects the user to the Auth0 authentication page for SSO login.
- The `logout_view` logs the user out of the Django session and redirects them to the Auth0 logout endpoint.
- The `callback` view processes the authentication response from Auth0 and handles user session management.
"""

from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login_view"), 
    path("sso-login", views.sso_login, name="sso_login"),  
    path("logout", views.logout_view, name="logout_view"), 
    path("callback", views.callback, name="callback"),  
]

