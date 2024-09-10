from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.contrib import messages
from users.models import User

# Initialize OAuth for Auth0 integration
oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,  # Auth0 client ID from settings
    client_secret=settings.AUTH0_CLIENT_SECRET,  # Auth0 client secret from settings
    client_kwargs={
        "scope": "openid profile email",  # Specify the scope of information we want from Auth0
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",  # Auth0 server metadata URL
)


def login_view(request):
    """
    Handle the login functionality.

    If the request method is POST, it authenticates the user using Django's built-in authentication.
    If authentication is successful, the user is logged in and redirected to the index page.
    Otherwise, an error message is displayed.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the login template or redirects on successful login.
    """
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)  # Django's built-in authentication
        
        if user is not None:
            django_login(request, user)  # Log the user in using Django's session system
            return redirect(reverse("index"))  # Redirect to index or dashboard
        else:
            messages.error(request, "Invalid email or password.")  # Display error message
    
    return render(request, 'authentication/index.html')  # Render the login page


def sso_login(request):
    """
    Initiate the Single Sign-On (SSO) login with Auth0.

    This function redirects the user to the Auth0 login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the Auth0 login page.
    """
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )


def callback(request):
    """
    Handle the callback from Auth0 after authentication.

    This function processes the token received from Auth0, retrieves user info,
    and logs the user in if they exist in the local database.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the index page after successful login.
    """
    token = oauth.auth0.authorize_access_token(request)  # Get the access token from Auth0
    userinfo = oauth.auth0.parse_id_token(request, token)  # Parse the user info from the token
    request.session["user"] = userinfo  # Store user info in session
    email = userinfo.get("email")  # Extract the user's email from the user info

    # If the user exists in the local database, log them in
    if check_existing_email(email):
        user = User.objects.get(email=email)
        django_login(request, user)  # Log the user in via Django's session system

    return redirect(reverse("index"))  # Redirect to the index page


def logout_view(request):
    """
    Handle the logout functionality.

    This function logs the user out of the Django session and clears the Auth0 session.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Redirects to the login page.
    """
    django_logout(request)  # Logout from Django session
    request.session.clear()  # Clear Auth0 session if any
    return redirect(reverse("login_view"))  # Redirect to login page


def check_existing_email(email):
    """
    Check if a user with the given email exists in the local database.

    Args:
        email (str): The user's email address.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    return User.objects.filter(email=email).exists()


@login_required
def index(request):
    """
    Render the index page for authenticated users.

    If the user is authenticated, it renders the index template with user session data.
    Otherwise, it returns a simple HTTP response indicating the user is not registered.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: Renders the index template or returns a simple response.
    """
    if request.user.is_authenticated:
        return render(
            request,
            "authentication/index.html",
            context={
                "session": request.session.get("user", {}),  # Pass user session data to the template
                "pretty": json.dumps(request.session.get("user", {}), indent=4),  # Pass prettified JSON of the session data
            },
        )
    else:
        return HttpResponse("User is not registered.")  # Return a simple response if user is not registered
