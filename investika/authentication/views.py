import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from django.http import HttpResponse
from users.models import User

# Initialize the OAuth object
oauth = OAuth()

# Register the Auth0 application with OAuth
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,  # Client ID from Auth0
    client_secret=settings.AUTH0_CLIENT_SECRET,  # Client Secret from Auth0
    client_kwargs={
        "scope": "openid profile email",  # Requested user info from Auth0
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",  # Auth0's OpenID configuration URL
)

# View for handling user login
def login(request):
    # Redirect the user to Auth0's authorization endpoint
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))  # Redirect to 'callback' after successful login
    )

# View for handling Auth0's callback (after authentication)
def callback(request):
    # Retrieve the access token from the authorization response
    token = oauth.auth0.authorize_access_token(request)
    
    # Store the token (which contains user info) in the session
    request.session["user"] = token
    
    # Redirect the user to the home page (index)
    return redirect(request.build_absolute_uri(reverse("index")))

# View for handling user logout
def logout(request):
    # Clear the session (logs the user out locally)
    request.session.clear()
    
    # Redirect the user to Auth0's logout endpoint and back to the home page
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),  # Redirect back to the index after logout
                "client_id": settings.AUTH0_CLIENT_ID,  # Pass the client ID to Auth0
            },
            quote_via=quote_plus,  # Ensure proper URL encoding
        ),
    )

# Helper function to check if a user with the given email exists in the local database
def check_existing_email(email):
    # Returns True if a user with the email exists, False otherwise
    return User.objects.filter(email=email).exists()

# View for the homepage (index)
def index(request):
    # Get the current user's session (if available)
    user = request.session.get("user")
    
    # If no user session exists, redirect to the login page
    if not user:
       return redirect(reverse("login"))
    
    # Extract the user's email from the session token
    email = user.get("email")
    
    # Check if the user with the extracted email exists in the database
    if not check_existing_email(email):
       # If the user is not registered, return an error message
       return HttpResponse("User is not registered.")
   
    # Render the homepage template, passing the session data and prettified user JSON as context
    return render(
        request,
        "authentication/index.html",  # Render the 'index.html' template
        context={
            "session": user,  # Pass the session object to the template
            "pretty": json.dumps(user, indent=4),  # Prettify the user session data for display
        },
    )
