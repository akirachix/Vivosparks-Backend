from django.urls import path
from . import views

# Define URL patterns for your app
urlpatterns = [
    # Home page route, maps the root URL ("/") to the `index` view
    path("", views.index, name="index"),  
    # Route for user login, maps the "/login" URL to the `login` view
    path("login", views.login, name="login"),  
    # Route for user logout, maps the "/logout" URL to the `logout` view
    path("logout", views.logout, name="logout"),  
    # Callback route, typically used for third-party authentication, maps the "/callback" URL to the `callback` view
    path("callback", views.callback, name="callback"),  
]
