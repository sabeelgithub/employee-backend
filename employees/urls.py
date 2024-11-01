from django.urls import path
from .views import *

urlpatterns = [
    path('create/',EmployeeCreate.as_view()),
    path('update/',EmployeeUpdate.as_view()),
    path('list/',EmployeeList.as_view()),
    path('delete/',EmployeeDelete.as_view()),
    path('single-employee/',SingleEmployeeOverview.as_view())
]
    
    