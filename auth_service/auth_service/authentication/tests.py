from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from . models import CustomUser
from unittest.mock import patch
from . jwt_helper import create_access_token, create_refresh_token


BLACK_LISTED_REFRESH_TOKEN = create_refresh_token(1)
VALID_ACCESS_TOKEN = create_access_token(1)

class CacheFixture():
    cache_storage = {
        BLACK_LISTED_REFRESH_TOKEN: "mock_user_data",
        VALID_ACCESS_TOKEN: "mock_user_data"
    }

    def set(self, key, value, timeout=None):
        self.cache_storage[key] = value

    def get(self, key, default=None):
        return self.cache_storage.get(key, default)
    
    def has_key(self, key):
        return key in self.cache_storage
    
    def delete(self, key, default=None):
        return self.cache_storage.pop(key, default)


class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')

    def test_register_view_success(self):
        # Create valid user data for registration
        data = {
            'email': 'test@email.com',
            'password': 'test_password',
            'first_name': 'test_firstname',
            'last_name': 'test_lastname',
            'is_manager': True
        }
        
        # Make a POST request to the register URL with the user data
        response = self.client.post(self.register_url, data)
   
        # Check the response status code and the created user in the database
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(CustomUser.objects.get().email, 'test@email.com')
    
    def test_register_view_invalid_data(self):
        # Create invalid user data for registration
        data = {
            'email': '',
            'password': 'testpassword',
        }
        
        # Make a POST request to the register URL with the invalid user data
        response = self.client.post(self.register_url, data)
        
        # Check the response status code and the error message in the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

class LoginViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')
        self.user = CustomUser.objects.create_user(
            email='test@email.com',
            password='test_password',
            first_name='test_firstname',
            last_name='test_lastname',
            is_manager=True
        )
    
    def test_login_view_success(self):
        # Create valid user login data
        data = {
            'email': 'test@email.com',
            'password': 'test_password',
            'first_name': 'test_firstname',
            'last_name': 'test_lastname',
            'is_manager': True
        }

        # Make a POST request to the login URL with the user login data
        response = self.client.post(self.login_url, data)
        
        # Check the response status code and the access token in the response cookies
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access_token', response.cookies)
        self.assertIn('refresh_token', response.cookies)
        
        # Verify the user data in the response
        self.assertEqual(response.data['user_id'], self.user.id)
        self.assertEqual(response.data['first_name'], self.user.first_name)
        self.assertEqual(response.data['last_name'], self.user.last_name)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['is_manager'], self.user.is_manager)
        
    def test_login_view_invalid_credentials(self):
        # Create invalid user login data
        data = {
            'email': 'test@email.com',
            'password': 'wrongpassword',
        }
        
        # Make a POST request to the login URL with the invalid user login data
        response = self.client.post(self.login_url, data)
        
        # Check the response status code and the error message in the response
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data['message'], 'invalid credentials')

    def test_login_view_invalid_data(self):
        # Create invalid user login data
        data = {
            'email': '',
            'password': 'wrongpassword',
        }      

        # Make a POST request to the login URL with the invalid user login data
        response = self.client.post(self.login_url, data)

        # Check the response status code and the error message in the response
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

class RefresfTokenViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.refresh_token_url = reverse('refresh_token')
        self.user = CustomUser.objects.create_user(
            email='test@email.com',
            password='test_password',
            first_name='test_firstname',
            last_name='test_lastname',
            is_manager=True
        )
        
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cache_fixture = CacheFixture()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.cache_fixture = None

    def test_refresh_token_view_success(self):
        # Set up a valid refresh token in the cookie
        refresh_token = create_refresh_token(self.user.id)
        self.client.cookies['refresh_token'] = refresh_token
        
        with patch('authentication.views.cache', self.cache_fixture) as mock_cache:
            # Make a GET request to the refresh_token URL
            response = self.client.get(self.refresh_token_url)
            
            # Check the response status code and the new access, refresh tokens in the response cookies
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertIn('access_token', response.cookies)
            self.assertIn('refresh_token', response.cookies)
            
            # Verify the user data in the response
            self.assertEqual(response.data['user_id'], self.user.id)
            self.assertEqual(response.data['first_name'], self.user.first_name)
            self.assertEqual(response.data['last_name'], self.user.last_name)
            self.assertEqual(response.data['email'], self.user.email)
            self.assertEqual(response.data['is_manager'], self.user.is_manager)

            # Check refresh token added to cache storage for blacklisting
            self.assertIn(refresh_token, mock_cache.cache_storage)

    def test_refresh_token_view_cookie_not_found(self):
        # Dont set up a cookie
        # Make a GET request to the refresh_token URL
        response = self.client.get(self.refresh_token_url)
        
        # Check the response status code and message
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Token is not found in cookie')

    def test_refresh_token_view_wrong_token_type(self):
        # Set up a access token in the cookie as a refresh token
        self.client.cookies['refresh_token'] = create_access_token(self.user.id)
        
        # Make a GET request to the refresh_token URL
        response = self.client.get(self.refresh_token_url)
        
        # Check the response status code and message
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'], 'Token type is not refresh')

    def test_refresh_token_view_token_for_not_exist_user(self):
        # Set up a refresh token with not exist user(user_id=5 doesnt exists)
        self.client.cookies['refresh_token'] = create_refresh_token(5)

        # Make a GET request to the refresh_token URL
        response = self.client.get(self.refresh_token_url)
        
        # Check the response status code and message
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('User not found', response.data['message'])

    def test_refresh_token_view_blacklisted(self):
        # Set up a blacklisted refresh token in the cookie
        self.client.cookies['refresh_token'] = BLACK_LISTED_REFRESH_TOKEN
        
        with patch('authentication.views.cache', self.cache_fixture):
            # Make a GET request to the refresh_token URL
            response = self.client.get(self.refresh_token_url)
            
            # Check the response status code and message
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.data['message'], 'Token is in Blacklist')

class CheckAccessTokenViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.check_token_url = reverse('check_access_token')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cache_fixture = CacheFixture()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.cache_fixture = None

    def test_check_view_success(self):
        # Set up a access token, which exists on cache, in the cookie
        self.client.cookies['access_token'] = VALID_ACCESS_TOKEN
        
        with patch('authentication.views.cache', self.cache_fixture):
            # Make a POST request to the register URL with the user data
            response = self.client.get(self.check_token_url)
    
            # Check the response status code and message
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data, "mock_user_data")

    def test_check_view_cookie_not_found(self):
        # Dont set up a token in cookie

        with patch('authentication.views.cache', self.cache_fixture):
            # Make a POST request to the register URL with the user data
            response = self.client.get(self.check_token_url)
    
            # Check the response status code and message
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.data['message'], 'Token is not found in cookie')

    def test_check_view_invalid_token(self):
        # Set up a access token, which doesnt exist on cache, in the cookie
        self.client.cookies['access_token'] = "acces_token_not_in_cache"

        with patch('authentication.views.cache', self.cache_fixture):
            # Make a POST request to the register URL with the user data
            response = self.client.get(self.check_token_url)
    
            # Check the response status code and message
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.data['message'], 'Token is not valid')

class LogoutViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.logout_url = reverse('logout')

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.cache_fixture = CacheFixture()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.cache_fixture = None

    def test_logout_view_success(self):
        # Set up a access token, which exists on cache, and refresh token in the cookie
        refresh_token = create_refresh_token(1)
        self.client.cookies['refresh_token'] = refresh_token
        self.client.cookies['access_token'] = VALID_ACCESS_TOKEN
        
        with patch('authentication.views.cache', self.cache_fixture) as mock_cache:
            # Make a POST request to the register URL with the user data
            response = self.client.get(self.logout_url)
    
            # Check the response status code and message
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['message'], "Logged out successfully!")

            # Check valid access token is not in cach anymore
            self.assertNotIn(VALID_ACCESS_TOKEN, mock_cache.cache_storage)
            # Check refresh token is blacklisted in cache
            self.assertIn(refresh_token, mock_cache.cache_storage)

            # Verify cookies are deleted
            self.assertEqual(response.cookies.get('access_token').value, '')
            self.assertEqual(response.cookies.get('refresh_token').value, '')

    def test_logout_view_success_only_access_token(self):
        # Set up a access token, which exists on cache, in the cookie
        refresh_token = create_refresh_token(1)

        self.client.cookies['access_token'] = VALID_ACCESS_TOKEN
        
        with patch('authentication.views.cache', self.cache_fixture) as mock_cache:
            # Make a POST request to the register URL with the user data
            response = self.client.get(self.logout_url)
    
            # Check the response status code and message
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['message'], "Logged out successfully!")

            # Check valid access token is not in cach anymore
            self.assertNotIn(VALID_ACCESS_TOKEN, mock_cache.cache_storage)

            # Verify cookies are deleted
            self.assertEqual(response.cookies.get('access_token').value, '')

    def test_logout_view_cookie_not_found(self):
        # Dont set up a token in cookie

        with patch('authentication.views.cache', self.cache_fixture):
            # Make a POST request to the register URL with the user data
            response = self.client.get(self.logout_url)
    
            # Check the response status code and message
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.data['message'], 'Token is not found in cookie')

    def test_logout_view_invalid_refresh_token(self):
        # Set up a access token, which exists on cache, in the cookie
        self.client.cookies['access_token'] = VALID_ACCESS_TOKEN
        self.client.cookies['refresh_token'] = 'invalid_refresh_token'
        
        with patch('authentication.views.cache', self.cache_fixture) as mock_cache:
            # Make a POST request to the register URL with the user data
            response = self.client.get(self.logout_url)

            # Check the response status code and message
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertIn('Invalid Refresh Token', response.data['message'])

            # Check valid access token is not in cach anymore
            self.assertNotIn(VALID_ACCESS_TOKEN, mock_cache.cache_storage)
            # Check invalid refresh token is not blacklisted in cache
            self.assertNotIn('invalid_refresh_token', mock_cache.cache_storage)

            # Verify cookies are deleted
            self.assertEqual(response.cookies.get('access_token').value, '')
            self.assertEqual(response.cookies.get('refresh_token').value, '')