from django.urls import path
from .views import *

urlpatterns = [
    path('create/',EmployeeCreate.as_view()),
    path('update/',EmployeeUpdate.as_view()),
    path('list/',EmployeeList.as_view()),
    path('delete/',EmployeeDelete.as_view()),
    path('single-employee/',SingleEmployeeOverview.as_view()),

    path('bad-coding-standards/',badCodingStandards.as_view()),
    path('complexity-logic-api/',ComplexLogicAPI.as_view()),
    path('dead-code-api/',DeadCodeAPI.as_view()),
    path('duplicate-code-api/',DuplicateCodeAPI.as_view()),
    path('bad-readability-api/',BadReadabilityAPI.as_view()),
    path('hard-coded-seceret-api/',HardcodedSecretsAPI.as_view()),
    path('security-issue-api/',SecurityIssueAPI.as_view()),
    path('perfomance-issue-api/',PerformanceIssueAPI.as_view()),
    path('bad-error-handling-api/',BadErrorHandlingAPI.as_view()),
    path('tightly-coupled-api/',TightlyCoupledAPI.as_view()),
]
    
    