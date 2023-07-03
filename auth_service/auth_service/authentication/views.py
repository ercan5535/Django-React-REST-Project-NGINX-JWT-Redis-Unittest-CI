import time

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from django.core.cache import cache
from django.conf import settings

from . models import CustomUser
from . jwt_helper import create_access_token, create_refresh_token, get_jwt_payload
from . serializers import UserRegisterSerializer, UserLoginSerializer

access_token_lifetime = settings.JWT["ACCESS_TOKEN_LIFETIME"].total_seconds()
refresh_token_lifetime = settings.JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()

class RegisterView(APIView):
    def post(self, request):  
        # Ensure username and passwords are posted is properly
        serializer = UserRegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        user = serializer.save()
        message = {'message': 'User registered successfully', 'user_id': user.id}
        return Response(message, status=status.HTTP_201_CREATED)

    
class LoginView(APIView):
    def post(self, request):
        # Ensure email and passwords are posted properly
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Check credentials
        user = authenticate(**serializer.data)
        if user is None:
            message = {"message": "invalid credentials"}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        
        # Create new access and refresh token
        access_token = create_access_token(user.id)
        refresh_token = create_refresh_token(user.id)

        # Add access token to redis for validating by other services
        user_data = {
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email" : user.email,
            "is_manager": user.is_manager
        }
        cache.set(access_token, user_data, access_token_lifetime)

        # Create response object
        response = Response(user_data, status=status.HTTP_201_CREATED)
        # Set access token in cookie
        response.set_cookie('access_token', access_token, httponly=True, expires=access_token_lifetime)
        # Set refresh token in cookie
        response.set_cookie('refresh_token', refresh_token, httponly=True, expires=refresh_token_lifetime)

        return response
    
class RefresfTokenView(APIView):
    def get(self, request):
        token = request.COOKIES.get('refresh_token')
        # Ensure token is in
        if token is None:
            message = {"message": "Token is not found in cookie"}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        
        # Ensure token is valid
        try:
            payload = get_jwt_payload(token)
        except Exception as e:
            message = {"message": "Invalid Token, " + str(e)}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        
        # Ensure user still exists
        try:
            user = CustomUser.objects.get(pk=payload["user_id"])
        except Exception as e:
            message = {"message": "User not found"+str(e)}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        
        # Ensure token is refresh token
        if payload["token_type"] != "refresh":
            message = {"message": "Token type is not refresh"}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

        # Check is token in Redis blacklist
        if cache.has_key(token):
            message = {"message": "Token is in Blacklist"}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

        # Create new access and refresh token
        access_token = create_access_token(payload["user_id"])
        refresh_token = create_refresh_token(payload["user_id"])

        # Add old refresh token to redis for blacklist check
        refresh_token_lifetime = payload["exp"] - time.time()
        cache.set(token, payload["user_id"], refresh_token_lifetime)

        # Add access token to redis for validating by other services
        user_data = {
            "user_id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email" : user.email,
            "is_manager": user.is_manager
        }
        cache.set(access_token, user_data, access_token_lifetime)

        # Create response object
        response = Response(user_data, status=status.HTTP_201_CREATED)
        # Set access token in cookie
        response.set_cookie('access_token', access_token, httponly=True, expires=access_token_lifetime)
        # Set refresh token in cookie
        response.set_cookie('refresh_token', refresh_token, httponly=True, expires=refresh_token_lifetime)
        return response

class CheckLoginStatus(APIView):
    def get(self, request):
        access_token = request.COOKIES.get('access_token')
    
        if access_token is None:
            message = {"message": "Token is not found in cookie"}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check is token in Redis 
        if not cache.has_key(access_token):
            message = {"message": "Token is not valid"}
            return Response(message, status=status.HTTP_401_UNAUTHORIZED)

        user_data = cache.get(access_token)

        return Response(user_data, status=status.HTTP_201_CREATED)

class Logout(APIView):
    def get(self, request):
        access_token = request.COOKIES.get('access_token')
        refresh_token = request.COOKIES.get('refresh_token')

        # Check access token is in cookie and access token is in Redis
        if access_token is not None and cache.has_key(access_token):
            # Delete access token from Redis
            cache.delete(access_token)
        
        # Check refresh token is in cookie
        if refresh_token is not None:
            # Ensure refresh token is valid
            try:
                payload = get_jwt_payload(refresh_token)
            except Exception as e:
                message = {"message": "Invalid Refresh Token, " + str(e)}
                return Response(message, status=status.HTTP_401_UNAUTHORIZED)
            # Check refresh token is not in Redis(Blacklist)
            if not cache.has_key(refresh_token):
                # Add refresh token to Redis blacklist
                cache.set(refresh_token, payload["user_id"])

        # Create response object
        message = {"message": "Logged out successfully!"}
        response = Response(message, status=status.HTTP_200_OK)
        # Delete access token from cookie
        response.delete_cookie('access_token')
        # Delete refresh token from cookie
        response.delete_cookie('refresh_token')
        return response
