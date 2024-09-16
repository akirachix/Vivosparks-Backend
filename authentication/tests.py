from unittest.mock import patch, MagicMock
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
import json

class AuthenticationTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('user_login')
        self.logout_url = reverse('logout')
        self.callback_url = reverse('callback')
        self.sso_login_url = reverse('login_sso')
        self.index_url = reverse('index')
        
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_success(self):
        response = self.client.post(self.login_url, json.dumps({
            'username': 'testuser',
            'password': 'testpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success', 'message': 'Logged in successfully!'})

    def test_login_failure(self):
        response = self.client.post(self.login_url, json.dumps({
            'username': 'testuser',
            'password': 'wrongpassword'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {'status': 'error', 'message': 'Invalid credentials'})

    # @patch('authlib.integrations.django_client.OAuth')
    # def test_login_sso_redirect(self, mock_oauth):
    #     mock_oauth.auth0.authorize_redirect.return_value = MagicMock(
    #         status_code=302,
    #         headers={'Location': 'https://dev-ukbw6mmqrbrekrgz.us.auth0.com/authorize?response_type=code&client_id=L3wIJ5y53AziBIJkWvptM1W4VaCgjues&redirect_uri=http%3A%2F%2Ftestserver%2Fauth%2Fcallback%2F&scope=openid+profile+email&state=mock_state&nonce=mock_nonce'}
    #     )
    #     response = self.client.get(self.sso_login_url)
    #     self.assertEqual(response.status_code, 302)
    #     self.assertTrue(response['Location'].startswith('https://dev-ukbw6mmqrbrekrgz.us.auth0.com/authorize'))

    
    @patch('authlib.integrations.django_client.OAuth')
    def test_callback_failure(self, mock_oauth):
        mock_oauth.auth0.authorize_access_token.side_effect = Exception('Failed')
        
        response = self.client.get(self.callback_url, {'state': 'mock_state'})
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'status': 'error', 'message': 'Failed to authorize'})

    def test_logout(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'status': 'success', 'message': 'User logged out successfully'})

    def test_index_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Welcome, testuser')

    def test_index_unauthenticated(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Welcome')
