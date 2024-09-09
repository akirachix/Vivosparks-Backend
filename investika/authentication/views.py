import json
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode
from django.http import HttpResponse
from users.models import User


"""
This module handles authentication using Auth0 integration and manages user sessions.
It includes views for login, callback (after successful authentication), logout, and index (user dashboard).
The Auth0 OAuth client is registered and configured using client credentials and server metadata.
The `login` function redirects the user to Auth0 for authentication.
The `callback` function processes the Auth0 response and stores the token in the session.
The `logout` function clears the session and redirects to the Auth0 logout endpoint.
The `index` function checks if the user is authenticated and whether their email exists in the database.
If the user is not registered, they are informed; otherwise, the user session is displayed.

"""

oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    userinfo = oauth.auth0.parse_id_token(request, token)
    request.session["user"] = userinfo
    return redirect(request.build_absolute_uri(reverse("index")))

def logout(request):
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

def check_existing_email(email):
    return User.objects.filter(email=email).exists()

def index(request):
    user = request.session.get("user")
    if not user:
     return redirect(reverse("login"))

    email = user.get("email") if isinstance(user, dict) else None

    if not check_existing_email(email):
        return HttpResponse("User is not registered.")
    
    return render(
        request,
        "authentication/index.html",
        context={
            "session": user,
            "pretty": json.dumps(user, indent=4),
        },
    )
