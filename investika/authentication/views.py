import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes


"""
Initialize OAuth for handling OAuth-based authentication, specifically for Auth0.
"""
oauth = OAuth()

"""
Register the OAuth provider, Auth0, with necessary credentials and configuration.
"""
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

"""
Set up the logger to capture and log messages for various activities within the views.
"""
logger = logging.getLogger(__name__)

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
import json
from django.contrib.auth import authenticate, login

@csrf_exempt
def user_login(request):
    """
    Handle user login with POST request. Authenticates using username and password.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        logger.info(f"Login attempt for username: {username}")

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            django_login(request, user)
            logger.info(f"User {username} logged in successfully.")
            return JsonResponse({'status': 'success', 'message': 'Logged in successfully!'}, status=200)
        else:
            logger.warning(f"Failed login attempt for username: {username}")
            return JsonResponse({'status': 'error', 'message': 'Invalid credentials'}, status=401)

    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=400)

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Handles password change requests. Ensures the user is authenticated and verifies the old password.
    If verification is successful, it sets a new password and updates the session.
    """
    logger.info(f"Request method: {request.method} received for password change.")
    
    if request.method == 'POST':
        logger.info(f"POST data received: {request.data}")

        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        logger.info(f"Password change attempt initiated by user: {user.username}")

        if user.check_password(old_password):
            logger.info(f"Old password verified for user: {user.username}")
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)

            logger.info(f"Password changed successfully for user: {user.username}")
            return JsonResponse({'status': 'success', 'message': 'Password changed successfully'}, status=200)
        else:
            logger.warning(f"Failed password change attempt for user: {user.username}. Incorrect old password provided.")
            return JsonResponse({'status': 'error', 'message': 'Old password is incorrect'}, status=400)

    logger.error(f"Invalid request method: {request.method} received for password change.")
    return JsonResponse({'status': 'error', 'message': 'Only POST requests are allowed'}, status=400)


@csrf_exempt
def loginSSO(request):
    """
    Initiates the Single Sign-On (SSO) login process by redirecting the user to the Auth0 authorization endpoint.
    """
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

@csrf_exempt
def callback(request):
    """
    Handles the OAuth callback after successful authentication with Auth0.
    Retrieves the access token and stores it in the session. Redirects to the index page.
    Logs any errors encountered during the process.
    """
    try:
        token = oauth.auth0.authorize_access_token(request)
        request.session["user"] = token

        logger.info("OAuth callback successful.")
        return redirect(request.build_absolute_uri(reverse("index")))
    except Exception as e:
        logger.error(f"Error during OAuth callback: {e}")
        return HttpResponse('Failed to authorize', status=400)

@csrf_exempt
def logout(request):
    """
    Logs the user out by clearing the session and redirecting them to the Auth0 logout endpoint.
    """
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )

def index(request):
    """
    Renders the index page, displaying the session information and user details (if logged in).
    """
    return render(
        request,
        "authentication/index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
        },
    )
