from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from . models import Transaction
from unittest.mock import patch


class TransactionViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.transactions_url = reverse('transactions')
        self.transaction1 = Transaction.objects.create(
            department='department1',
            amount=100,
            created_by='user1',
            is_confirmed=False
        )
        self.transaction2 = Transaction.objects.create(
            department='department2',
            amount=200,
            created_by='user2',
            is_confirmed=True
        )
        self.new_transaction_data = {
            'department': 'department3',
            'amount': 300,
            'created_by': 'user3'
        }

    def test_transaction_view_invalid_token(self):
        # Set up a valid access token in the cookie
        self.client.cookies['access_token'] = 'my_access_token'
        with patch('transactions.views.cache') as mock_cache:
            # Mock cache for token_required check is wrong
            mock_cache.has_key.return_value = False

            # Make a GET request to the transactions URL
            get_response = self.client.get(self.transactions_url)
    
            # Check the response status code
            self.assertEqual(get_response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(get_response.data['message'], 'Unauthorized')

            # Make a GET request to the transactions URL
            post_response = self.client.post(self.transactions_url, self.new_transaction_data)
    
            # Check the response status code
            self.assertEqual(post_response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(post_response.data['message'], 'Unauthorized')

    def test_transaction_view_no_cookie(self):
        # Dont set up a cookie
        
        # Make a GET request to the transactions URL
        get_response = self.client.get(self.transactions_url)

        # Check the response status code
        self.assertEqual(get_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(get_response.data['message'], 'Unauthorized')

        # Make a POST request to the transactions URL
        post_response = self.client.post(self.transactions_url, self.new_transaction_data)

        # Check the response status code
        self.assertEqual(post_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(post_response.data['message'], 'Unauthorized')

    def test_transaction_view_get_success(self):
        # Set up a valid access token in the cookie
        self.client.cookies['access_token'] = 'my_access_token'
        with patch('transactions.views.cache') as mock_cache:
            # Mock cache for token_required check is correct
            mock_cache.has_key.return_value = True

            # Make a POST request to the transactions URL
            response = self.client.get(self.transactions_url)
    
            # Check the response status code
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(len(response.data), 2)


    def test_transaction_view_post_success(self):
        # Set up a valid access token in the cookie
        self.client.cookies['access_token'] = 'my_access_token'

        with patch('transactions.views.cache') as mock_cache:
            # Mock cache for token_required check is correct
            mock_cache.has_key.return_value = True

            # Make a POST request to the transactions URL
            response = self.client.post(self.transactions_url, self.new_transaction_data)
    
            # Check the response status code
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data['created_by'], 'user3')
            # Check total count is incremented to 3
            self.assertEqual(Transaction.objects.count(), 3)

    def test_transaction_view_post_invalid_data(self):
        # Set up a valid access token in the cookie
        self.client.cookies['access_token'] = 'my_access_token'

        invalid_data = {
            'department': '',
            'amount': 300,
            'created_by': 'user1'
        }

        with patch('transactions.views.cache') as mock_cache:
            # Mock cache for token_required check is correct
            mock_cache.has_key.return_value = True

            # Make a POST request to the transactions URL
            response = self.client.post(self.transactions_url, invalid_data)
    
            # Check the response status code
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('department', response.data)

class TransactionDetailViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.transaction1 = Transaction.objects.create(
            department='department1',
            amount=100,
            created_by='user1'
        )
        self.transaction2 = Transaction.objects.create(
            department='department2',
            amount=200,
            created_by='user2'
        )
        self.new_transaction_data = {
            'department': 'department3',
            'amount': 300,
            'created_by': 'user3'
        }

    def test_transaction_detail_view_invalid_token(self):
        # Set up a valid access token in the cookie
        self.client.cookies['access_token'] = 'my_access_token'
        # Set url for id=1
        transaction_detail_url = reverse('transaction_detail', args=[1])
        with patch('transactions.views.cache') as mock_cache:
            # Mock cache for token_required check is wrong
            mock_cache.has_key.return_value = False

            # Make a GET request to the transactions URL
            get_response = self.client.get(transaction_detail_url)
    
            # Check the response status code
            self.assertEqual(get_response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(get_response.data['message'], 'Unauthorized')

            # Make a PATCH request to the transactions URL
            patch_response = self.client.patch(transaction_detail_url, self.new_transaction_data)
    
            # Check the response status code
            self.assertEqual(patch_response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(patch_response.data['message'], 'Unauthorized')

            # Make a DELETE request to the transactions URL
            delete_response = self.client.delete(transaction_detail_url)
    
            # Check the response status code
            self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(delete_response.data['message'], 'Unauthorized')

            # Make a HEAD request to the transactions URL
            head_response = self.client.head(transaction_detail_url)
    
            # Check the response status code
            self.assertEqual(head_response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(head_response.data['message'], 'Unauthorized')

    def test_transaction_detail_no_cookie(self):
        # Set url for id=1
        transaction_detail_url = reverse('transaction_detail', args=[1])
        
        # Make a GET request to the transactions URL
        get_response = self.client.get(transaction_detail_url)

        # Check the response status code
        self.assertEqual(get_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(get_response.data['message'], 'Unauthorized')

        # Make a PATCH request to the transactions URL
        patch_response = self.client.patch(transaction_detail_url, self.new_transaction_data)

        # Check the response status code
        self.assertEqual(patch_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(patch_response.data['message'], 'Unauthorized')

        # Make a DELETE request to the transactions URL
        delete_response = self.client.delete(transaction_detail_url)

        # Check the response status code
        self.assertEqual(delete_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(delete_response.data['message'], 'Unauthorized')

        # Make a HEAD request to the transactions URL
        head_response = self.client.head(transaction_detail_url)

        # Check the response status code
        self.assertEqual(head_response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(head_response.data['message'], 'Unauthorized')

    def test_transaction_detail_transaction_not_found(self):
        # Set url for id=5(Not exists)
        transaction_detail_url = reverse('transaction_detail', args=[5])
        # Set up a valid access token in the cookie
        self.client.cookies['access_token'] = 'my_access_token'
        with patch('transactions.views.cache') as mock_cache:
            # Mock cache for token_required check is correct
            mock_cache.has_key.return_value = True
            # Make a GET request to the transactions URL
            get_response = self.client.get(transaction_detail_url)

            # Check the response status code
            self.assertEqual(get_response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(get_response.data['message'], 'transaction not found')

            # Make a PATCH request to the transactions URL
            patch_response = self.client.patch(transaction_detail_url, self.new_transaction_data)

            # Check the response status code
            self.assertEqual(patch_response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(patch_response.data['message'], 'transaction not found')

            # Make a DELETE request to the transactions URL
            delete_response = self.client.delete(transaction_detail_url)

            # Check the response status code
            self.assertEqual(delete_response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(delete_response.data['message'], 'transaction not found')

            # Make a HEAD request to the transactions URL
            head_response = self.client.head(transaction_detail_url)

            # Check the response status code
            self.assertEqual(head_response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(head_response.data['message'], 'transaction not found')

    def test_transaction_detail_get_succes(self):
        # Set up a valid access token in the cookie
        self.client.cookies['access_token'] = 'my_access_token'
        with patch('transactions.views.cache') as mock_cache:
            # Mock cache for token_required check is correct
            mock_cache.has_key.return_value = True

            # Set url for id=1
            transaction_detail_url = reverse('transaction_detail', args=[1])

            # Make a GET request to the transactions URL
            response = self.client.get(transaction_detail_url)

            # Check the response status code
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['department'], 'department1')
            self.assertEqual(response.data['amount'], 100)
            self.assertEqual(response.data['created_by'], 'user1')

            # Set url for id=2
            transaction_detail_url = reverse('transaction_detail', args=[2])

            # Make a GET request to the transactions URL
            response = self.client.get(transaction_detail_url)

            # Check the response status code
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['department'], 'department2')
            self.assertEqual(response.data['amount'], 200)
            self.assertEqual(response.data['created_by'], 'user2')

    def test_transaction_detail_patch_succes(self):
        # Set up a valid access token in the cookie
        self.client.cookies['access_token'] = 'my_access_token'
        data={'department': 'new_department'}

        with patch('transactions.views.cache') as mock_cache:
            # Mock cache for token_required check is correct
            mock_cache.has_key.return_value = True

            # Set url for id=1
            transaction_detail_url = reverse('transaction_detail', args=[1])

            # Make a PATCH request to the transactions URL
            response = self.client.patch(transaction_detail_url, data)

            # Check the response status code
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['department'], 'new_department')
            self.assertEqual(response.data['amount'], 100)
            self.assertEqual(response.data['created_by'], 'user1')

            # Set url for id=2
            transaction_detail_url = reverse('transaction_detail', args=[2])

            # Make a PATCH request to the transactions URL
            response = self.client.patch(transaction_detail_url, data)

            # Check the response status code
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['department'], 'new_department')
            self.assertEqual(response.data['amount'], 200)
            self.assertEqual(response.data['created_by'], 'user2')

    def test_transaction_detail_patch_invalid_data(self):
        # Set up a valid access token in the cookie
        self.client.cookies['access_token'] = 'my_access_token'
        data={'amount': 'string_for_amount'}

        with patch('transactions.views.cache') as mock_cache:
            # Mock cache for token_required check is correct
            mock_cache.has_key.return_value = True
            
            # Set url for id=1
            transaction_detail_url = reverse('transaction_detail', args=[1])

            # Make a PATCH request to the transactions URL
            response = self.client.patch(transaction_detail_url, data)

            # Check the response status code
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn('amount', response.data)

    def test_transaction_detail_delete_succes(self):
        # Set up a valid access token in the cookie
        self.client.cookies['access_token'] = 'my_access_token'
        data={'department': 'new_department'}

        with patch('transactions.views.cache') as mock_cache:
            # Mock cache for token_required check is correct
            mock_cache.has_key.return_value = True
            
            # Set url for id=1
            transaction_detail_url = reverse('transaction_detail', args=[1])

            # Make a DELETE request to the transactions URL
            response = self.client.delete(transaction_detail_url, data)

            # Check the response status code
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Transaction.objects.filter(pk=1).exists(), False)

            # Set url for id=2
            transaction_detail_url = reverse('transaction_detail', args=[2])

            # Make a DELETE request to the transactions URL
            response = self.client.delete(transaction_detail_url, data)

            # Check the response status code
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(Transaction.objects.filter(pk=2).exists(), False)


    def test_transaction_detail_head_succes(self):
        # Set up a valid access token in the cookie
        self.client.cookies['access_token'] = 'my_access_token'

        with patch('transactions.views.cache') as mock_cache:
            # Mock cache for user_data is manager=True
            mock_cache.has_key.return_value = True
            mock_cache.get.return_value = {'is_manager': True}
            
            # Set url for id=1
            transaction_detail_url = reverse('transaction_detail', args=[1])

            # Make a HEAD request to the transactions URL
            response_confirm = self.client.head(transaction_detail_url)

            # Check the response status code
            self.assertEqual(response_confirm.status_code, status.HTTP_200_OK)
            self.assertEqual(Transaction.objects.get(pk=1).is_confirmed, True)

            # Make a HEAD request to the transactions URL
            response_unconfirm = self.client.head(transaction_detail_url)

            # Check the response status code
            self.assertEqual(response_unconfirm.status_code, status.HTTP_200_OK)
            self.assertEqual(Transaction.objects.get(pk=1).is_confirmed, False)



    def test_transaction_detail_head_not_manager(self):
        # Set up a valid access token in the cookie
        self.client.cookies['access_token'] = 'my_access_token'

        with patch('transactions.views.cache') as mock_cache:
            # Mock cache for user_data is manager=True
            mock_cache.has_key.return_value = True
            mock_cache.get.return_value = {'is_manager': False}
            
            # Set url for id=1
            transaction_detail_url = reverse('transaction_detail', args=[1])

            # Make a PATCH request to the transactions URL
            response = self.client.head(transaction_detail_url)

            # Check the response status code
            self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
            self.assertEqual(response.data['message'], 'Unauthorized')