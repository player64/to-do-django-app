import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase


class UserLoginTest(APITestCase):
    def setUp(self):
        self.login_url = reverse('user-login')
        self.userModel = get_user_model()

    def test_api_login_with_credentials(self):
        self.userModel.objects.create_user(email='test@test.com', password='password', name='test tester')
        response = self.client.post(self.login_url, {
            'email': 'test@test.com',
            'password': 'password'
        }, follow=True)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('access' in response_json and 'refresh' in response_json)

    def test_api_login_with_wrong_password(self):
        self.userModel.objects.create_user(email='test@test1.com', password='password', name='test tester')
        response = self.client.post('/api/v1/users/login/', {
            'email': 'test@test1.com',
            'password': 'test_password'
        })
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), {'detail': 'No active account found with the given credentials'})

    def test_protected_route_without_token(self):
        url = reverse('protected-view')
        response = self.client.get(url)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(content, {'detail': 'Authentication credentials were not provided.'})

    def test_protected_route_with_token(self):
        url = reverse('protected-view')
        self._authenticate()
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'message': 'This view should be only accessible with Barer Token'})

    def test_logout(self):
        token = self._authenticate()
        response = self.client.post(reverse('user-logout'), {
            'refresh': token['refresh']
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'Successfully logged out'})

        # check is the token is blacklisted
        response = self.client.post(reverse('token-refresh'), {
            'refresh': token['refresh']
        })
        self.assertEqual(response.json(), {'detail': 'Token is blacklisted', 'code': 'token_not_valid'})
        self.assertEqual(response.status_code, 401)

    def test_refresh_token(self):
        tokens = self._authenticate()
        access_token = tokens['access']

        response = self.client.post(reverse('token-refresh'), {
            'refresh': tokens['refresh']
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()['access'] != access_token)

    def _authenticate(self):
        self.userModel.objects.create_user(email='email@email.com', password='password', name='test tester')
        response = self.client.post('/api/v1/users/login/', {
            'email': 'email@email.com',
            'password': 'password'
        }, follow=True)
        tokens = response.json()
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(tokens['access']))
        return tokens
