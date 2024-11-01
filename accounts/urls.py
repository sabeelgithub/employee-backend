from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('create/',RegisterView.as_view()),
    path('login/',Login.as_view()),
    path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh')

]
    