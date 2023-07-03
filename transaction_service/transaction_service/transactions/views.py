from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from . models import Transaction
from . serializers import TransactionSerializer
from django.core.cache import cache
from django.conf import settings

# Define decorator to check access token in redis
def token_required(view_func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')

        if access_token is not None and cache.has_key(access_token):
            return view_func(self, request, *args, **kwargs)
        
        return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
    return wrapper

# Define decorator to check user is manager
def manager_required(view_func):
    def wrapper(self, request, *args, **kwargs):
        access_token = request.COOKIES.get('access_token')

        if access_token is not None and cache.has_key(access_token):
            user_data = cache.get(access_token)
            if user_data["is_manager"]:
                return view_func(self, request, *args, **kwargs)
        
        return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)
    return wrapper

class TransactionView(APIView):
    # Get all transactions
    @token_required
    def get(self, request):
        obj = Transaction.objects.all().order_by('-created_at')
        serializer = TransactionSerializer(obj, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Create new transaction
    @token_required
    def post(self, request):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionDetailView(APIView):
    def get_object(self, pk):
        try:
            transaction = Transaction.objects.get(pk=pk)
            return transaction
        except:
            return None
    
    # Get single transaction details with id
    @token_required
    def get(self, request, pk):
        transaction = self.get_object(pk)
        if transaction is None:
            message = {"message": "transaction not found "}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        serializer = TransactionSerializer(transaction)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # Update a transaction with id
    @token_required
    def patch(self, request, pk):
        transaction = self.get_object(pk)
        if transaction is None:
            message = {"message": "transaction not found "}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        serializer = TransactionSerializer(transaction, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a transaction with id
    @token_required
    def delete(self, request, pk):
        transaction = self.get_object(pk)
        if transaction is None:
            message = {"message": "transaction not found "}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)

        transaction.delete()
        message = {"message": "transaction deleted"}
        return Response(message, status=status.HTTP_200_OK)
    
    # Confirm a transaction with id
    @manager_required
    def head(self, request, pk):
        transaction = self.get_object(pk)
        if transaction is None:
            message = {"message": "transaction not found "}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        
        transaction.is_confirmed = not transaction.is_confirmed
        transaction.save()

        return Response(status=status.HTTP_200_OK)



