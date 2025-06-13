import unittest
from django.urls import reverse
from rest_framework.test import APIClient, APITestCase, force_authenticate, APIRequestFactory
from rest_framework import status
from api_applications.accounts.models import CustomUser, UserProfile
from django.contrib.auth import get_user_model
from django.db import transaction
from api_applications.accounts.views import UserProfileAPIView

User = get_user_model()

class AuthenticationTest(APITestCase):
    def setUp(self):
        """
        Set up test environment before each test method
        """
        self.client = APIClient()
        self.factory = APIRequestFactory()
        self.login_url = reverse('token_obtain_pair')
        self.register_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        self.login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }

    def test_user_registration(self):
        """Test user registration and automatic profile creation"""
        with transaction.atomic():
            user = User.objects.create_user(
                username=self.register_data['username'],
                email=self.register_data['email'],
                password=self.register_data['password']
            )
            
            # Check if user was created successfully
            self.assertTrue(isinstance(user, CustomUser))
            self.assertEqual(user.email, self.register_data['email'])
            
            # Check if UserProfile was automatically created
            profile = UserProfile.objects.filter(user=user).first()
            self.assertIsNotNone(profile)
            self.assertTrue(isinstance(profile, UserProfile))

    def test_user_login(self):
        """Test user login and token generation"""
        with transaction.atomic():
            User.objects.create_user(
                username=self.register_data['username'],
                email=self.register_data['email'],
                password=self.register_data['password']
            )
            
            # Attempt login
            response = self.client.post(self.login_url, self.login_data)
            
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue('access' in response.cookies)
            self.assertTrue('refresh' in response.cookies)

    def test_invalid_login(self):
        """Test login with invalid credentials"""
        invalid_data = {
            'username': 'wronguser',
            'password': 'wrongpass'
        }
        response = self.client.post(self.login_url, invalid_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_profile_access(self):
        """Test accessing user profile with token authentication"""
        with transaction.atomic():
            # Create user
            user = User.objects.create_user(
                username=self.register_data['username'],
                email=self.register_data['email'],
                password=self.register_data['password']
            )
            
            # Force authenticate the user
            self.client.force_authenticate(user=user)

            # Access profile
            profile_url = reverse('user-profile')
            response = self.client.get(profile_url)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.json()['user'], user.username)

    def test_user_profile_with_factory(self):
        """Test user profile access using APIRequestFactory"""
        with transaction.atomic():
            # Create user
            user = User.objects.create_user(
                username=self.register_data['username'],
                email=self.register_data['email'],
                password=self.register_data['password']
            )

            # Create profile request
            profile_request = self.factory.get('/api/profile/')
            force_authenticate(profile_request, user=user)
            profile_view = UserProfileAPIView.as_view()
            profile_response = profile_view(profile_request)
                        
            self.assertEqual(profile_response.status_code, status.HTTP_200_OK)
            response_data = profile_response.data
            self.assertEqual(response_data['user'], user.username)


if __name__ == '__main__':
    unittest.main()
