import json
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


def _create_register_data_with_password(password):
    return {
        "email": "test@test.com",
        "password": password,
        "repeat_password": password,
        "name": "Test User"
    }


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('user-register')

    def test_user_registration(self):
        data = _create_register_data_with_password('Testp@ssword123')
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 201)
        User = get_user_model()
        user = User.objects.get(email=data['email'])
        self.assertEqual(user.name, data['name'])

    def test_user_registration_wrong_repeat_password(self):
        data = {
            "email": "test@test.com",
            "password": "testpassword1",
            "repeat_password": "testpassword",
            "name": "Test User"
        }
        response = self.client.post(self.register_url, data)
        response_json = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response_json['non_field_errors'][0], 'Passwords must match.')

    def test_password_policy_correct_errors(self):
        wrong_passwords = [
            # length less than 8 characters
            {
                'data': _create_register_data_with_password('abcd'),
                'expected_errors': [
                    'Password must be at least 8 characters.',
                    'Password must contain at least one digit.',
                    'Password must contain at least one uppercase letter.',
                    'Password must contain at least one special character.'
                ]
            },
            # one numeric
            {
                'data': _create_register_data_with_password('1password'),
                'expected_errors': [
                    'Password must contain at least one uppercase letter.',
                    'Password must contain at least one special character.'
                ]
            },
            # all numeric
            {
                'data': _create_register_data_with_password('12345678'),
                'expected_errors': [
                    'Password must contain at least one letter.',
                    'Password must contain at least one uppercase letter.',
                    'Password must contain at least one special character.'
                ]
            },
            # no special character
            {
                'data': _create_register_data_with_password('1Password'),
                'expected_errors': [
                    'Password must contain at least one special character.'
                ]
            },
        ]

        for wrong_password in wrong_passwords:
            data = wrong_password['data']
            response = self.client.post(self.register_url, data)
            self.assertEqual(response.status_code, 400)
            response_json = json.loads(response.content)
            self.assertListEqual(response_json['non_field_errors'], wrong_password['expected_errors'])
