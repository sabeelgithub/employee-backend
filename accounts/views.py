from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from  rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status


from .serializers import UserWriteSerializer
from .helpers import (
    username_already_exists,
    email_already_exists,
    phone_already_exists,
    password_length_issue,
    user_create_success
)
from utils import (
    internal_server_error_response,
    invalid_inputs
)

class RegisterView(APIView):
    @swagger_auto_schema(
    operation_description="Create User",
    operation_id='create user',
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