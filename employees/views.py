from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from  rest_framework_simplejwt.authentication import JWTAuthentication
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status


from utils import (
    internal_server_error_response
)
class Check(APIView):
    def get(self,request):
        try:
            return Response({"message":"checking","status":status.HTTP_200_OK},status=status.HTTP_200_OK)
        except Exception as e:
            return Response(internal_server_error_response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)