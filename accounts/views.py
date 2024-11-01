from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from  rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth.hashers import check_password

from .serializers import (
    UserWriteSerializer,
    UserReadSerializer,
    LoginSerializer,
    TokenRefreshSerializer,
    ChangePasswordSerializer
    )
from utils import (
    internal_server_error_response,
    invalid_inputs
)
from .helpers import (
    username_already_exists,
    email_already_exists,
    phone_already_exists,
    password_length_issue,
    user_create_success,
    invalid_username_or_password,
    login_success,
    new_refresh_token_create_success,
    invalid_refresh_token,
    user_password_change_success,
    user_password_does_not_match,
    user_password_same_as_previous,
    user_detail_success
)
from .models import CustomUser

class RegisterView(APIView):
    @swagger_auto_schema(
    operation_description="Register",
    operation_id='register',
    request_body=UserWriteSerializer
    )
    def post(self, request):
        try:
            serializer = UserWriteSerializer(data=request.data)
            if not serializer.is_valid():
                if serializer.errors.get('username') and  serializer.errors.get('username') == ["user with this username already exists."]:
                    return Response(username_already_exists(),status=status.HTTP_409_CONFLICT)
                        
                if serializer.errors.get('email') and  serializer.errors.get('email') == ["user with this email address already exists."]:
                    return Response(email_already_exists(),status=status.HTTP_409_CONFLICT)
                    
                if serializer.errors.get('phone') and  serializer.errors.get('phone') == ["user with this phone already exists."]:
                    return Response(phone_already_exists(),status=status.HTTP_409_CONFLICT)
                
                if serializer.errors.get('password'):
                    return Response(password_length_issue(),status=status.HTTP_400_BAD_REQUEST)
                
                return Response(invalid_inputs(serializer.errors),status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()
            return Response(user_create_success(serializer.data),status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response(internal_server_error_response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Login(APIView):

    # function for login
    @swagger_auto_schema(
    operation_description="Login",
    operation_id='login',
    request_body=LoginSerializer
    )
    def post(self,request):
        try:
            username = request.data['username']
            password = request.data['password']
            user = authenticate(request,username=username,password=str(password))
            if user is not None:
                login(request,user)
                refresh = RefreshToken.for_user(user)
                data = {
                    'access_token':str(refresh.access_token),
                    'refresh_token':str(refresh)
                }
                return Response(login_success(data),status=status.HTTP_200_OK)
            
            return Response(invalid_username_or_password(),status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(internal_server_error_response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyTokenRefreshView(TokenRefreshView):
    # function for getting new acces and refresh token
    @swagger_auto_schema(
    operation_description="New Token",
    operation_id='new token',
    request_body=TokenRefreshSerializer
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            # Handle validation errors here
            return Response(invalid_refresh_token(e),status=status.HTTP_400_BAD_REQUEST)
        data = {'access_token':serializer.validated_data['access'],
                    'refresh_token': serializer.validated_data['refresh']}
        return Response(new_refresh_token_create_success(data),status=status.HTTP_200_OK)


class ChangePassword(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # function for changing password
    @swagger_auto_schema(
    operation_description="Change Password",
    operation_id='change password',
    request_body=ChangePasswordSerializer
    ) 
    def post(self,request):
        try:
            current_password = str(request.data.get("current_password"))
            new_password = str(request.data.get("new_password"))
            
            if len(new_password) < 5:
                return Response(password_length_issue(),status=status.HTTP_400_BAD_REQUEST)
            
            if not check_password(current_password,request.user.password):
                return Response(user_password_does_not_match(),status=status.HTTP_400_BAD_REQUEST)
            
            if check_password(new_password,request.user.password):
                return Response(user_password_same_as_previous(),status=status.HTTP_400_BAD_REQUEST)
            
            user = CustomUser.objects.get(id=request.user.id)
            user.set_password(str(new_password))
            user.save()
            return Response(user_password_change_success(),status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(internal_server_error_response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class UserProfileData(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # function for  user profile data 
    @swagger_auto_schema(
    operation_description="User Profile",
    operation_id='user profile'
    )       
    def get(self,request):
        try:
            user = CustomUser.objects.get(id=request.user.id)
            serializer = UserReadSerializer(user)
            return Response(user_detail_success(serializer.data),status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(internal_server_error_response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)