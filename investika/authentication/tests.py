from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.conf import settings
from unittest.mock import patch
import json

class AuthViewsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'securepassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
    
    def test_user_login_success(self):
        response = self.client.post('/auth/login/', json.dumps({'username': self.username, 'password': self.password}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success', 'message': 'Logged in successfully!'})
    
    def test_user_login_failure(self):
        response = self.client.post('/auth/login/', json.dumps({'username': self.username, 'password': 'wrongpassword'}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {'status': 'error', 'message': 'Invalid credentials'})
    
    @patch('authlib.integrations.django_client.OAuth')
    def test_login_sso(self, mock_oauth):
        mock_oauth.return_value.auth0.authorize_redirect.return_value = 'redirect_url'
        response = self.client.get('/auth/sso-login/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], 'redirect_url')
    
    @patch('authlib.integrations.django_client.OAuth')
    def test_callback_success(self, mock_oauth):
        mock_oauth.return_value.auth0.authorize_access_token.return_value = {'access_token': 'token'}
        response = self.client.get('/auth/callback/?code=test_code&state=test_state')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('index'))
    
    @patch('authlib.integrations.django_client.OAuth')
    def test_callback_failure(self, mock_oauth):
        mock_oauth.return_value.auth0.authorize_access_token.side_effect = Exception('Auth Error')
        response = self.client.get('/auth/callback/?code=test_code&state=test_state')
        self.assertEqual(response.status_code, 400)
    
    def test_logout(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post('/auth/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success', 'message': 'User logged out successfully'})
        
        # Ensure the session is cleared
        response = self.client.get('/auth/')
        self.assertNotContains(response, 'User logged in successfully!')

