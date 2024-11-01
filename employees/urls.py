from django.urls import path
from .views import *

urlpatterns = [
    path('check/',Check.as_view()),
]
    
    