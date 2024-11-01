from django.urls import path
from .views import *

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('create/',RegisterView.as_view()),
    # path('', views.index,name='home'),
    # path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', MyTokenRefreshView.as_view(), name='token_refresh'),
]
    