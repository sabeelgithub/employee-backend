from rest_framework.views import APIView
from rest_framework.response import Response
from  rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from drf_yasg import openapi

from utils import (
    internal_server_error_response,
    invalid_inputs,
    pagination_processing,
    filtration_processing
)
from .serializers import (
    EmployeeWriteSerializer,
    EmployeeReadSerializer
)
from .helpers import (
    employee_create_success,
    employee_update_success,
    employee_not_found,
    employee_success_list,
    employee_delete_success,
    employee_detail_success
)
from .models import Employee
        
class EmployeeCreate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
    operation_description="Create Eemployee",
    operation_id="employee create",
    request_body=EmployeeWriteSerializer
    )
    def post(self,request):
        try:
            serializer = EmployeeWriteSerializer(data=request.data,context={"user":request.user})
            if not serializer.is_valid():
                return Response(invalid_inputs(serializer.errors),status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()        
            return Response(employee_create_success(serializer.data),status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response(internal_server_error_response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EmployeeUpdate(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
    operation_description="Update Employee",
    operation_id="employee update",
    request_body=EmployeeWriteSerializer,
    manual_parameters=[
            openapi.Parameter('id', 
            openapi.IN_QUERY, 
            description="Employee ID", 
            type=openapi.TYPE_STRING,
            required=True
            )
        ]
    ) 
    def patch(self,request):
        try:
            employee_id = request.GET.get('id')
            instance = Employee.objects.get(id=employee_id)
            serializer = EmployeeWriteSerializer(instance=instance,data=request.data) 
            if not serializer.is_valid():
                return Response(invalid_inputs(serializer.errors),status=status.HTTP_400_BAD_REQUEST)
              
            serializer.save()
            return Response(employee_update_success(),status=status.HTTP_200_OK)
        
        except Employee.DoesNotExist:
            return Response(employee_not_found(),status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(internal_server_error_response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class EmployeeList(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
    operation_description="Employee List",
    operation_id="employee list"
    )     
    def post(self,request):
        try:
            filtration_data = request.data.get("filtration_data",None)
            pagination_data = request.data.get("pagination",None)

            q_object = filtration_processing(filtration_data)
            employees = Employee.objects.filter(*q_object,user=request.user).order_by('-created_at')
            employees_count = employees.count()
            paged_employees = pagination_processing(pagination_data,employees)

            if paged_employees["status"] == status.HTTP_200_OK:
                serializer = EmployeeReadSerializer(paged_employees["data"],many=True)
                return Response(employee_success_list({"row_data":serializer.data,"count":employees_count}),status=status.HTTP_200_OK)
            return Response(paged_employees,status=status.HTTP_404_NOT_FOUND)
        
        except Employee.DoesNotExist:
            return Response(employee_not_found(),status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(internal_server_error_response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class EmployeeDelete(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
    operation_description="Employee Delete",
    operation_id='delete employee',
    manual_parameters=[
        openapi.Parameter('id', 
        openapi.IN_QUERY, 
        description="Employee ID", 
        type=openapi.TYPE_STRING,
        required=True
        )
      ]
    )
    def delete(self,request):
        try:
            employee_id = request.GET.get('id')
            employee = Employee.objects.get(id=employee_id)
            employee.delete()
            return Response(employee_delete_success(),status=status.HTTP_200_OK)

        except Employee.DoesNotExist:
            return Response(employee_not_found(),status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(internal_server_error_response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class SingleEmployeeOverview(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
    operation_description="Single Employee Record",
    operation_id="single employee",
    manual_parameters=[
            openapi.Parameter('id', 
            openapi.IN_QUERY, 
            description="Employee ID", 
            type=openapi.TYPE_STRING,
            required=True
            )
        ]
    ) 
    def get(self,request):
        try:
            employee_id = request.GET.get('id')
            role = Employee.objects.get(id=employee_id)
            serializer = EmployeeReadSerializer(role)
            return Response(employee_detail_success(serializer.data),status=status.HTTP_200_OK)
        
        except Employee.DoesNotExist:
            return Response(employee_not_found(),status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response(internal_server_error_response(e),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

# ===============================================================
# 1. BAD CODING STANDARDS & BEST PRACTICES VIOLATIONS
# ===============================================================

from django.db import connection   # Unused
import json, re, datetime, random  # Many unused imports (flagged)

class badCodingStandards(APIView):   # Class name should be PascalCase
    def get(self,REQUEST):           # Parameter name should be lowercase (flagged)
        a=1      # Inconsistent spacing
        A=2      # Bad naming
        someVariable = 10
        some_variable = 20
        SomeVariable = 30

        x = someVariable + some_variable + SomeVariable

        return Response({"data":x})
    

# ===============================================================
# 2. CYCLICALLY COMPLEX FUNCTION (Cyclomatic Complexity)
# ===============================================================

class ComplexLogicAPI(APIView):
    def get(self, request):

        value = request.GET.get("value")

        # Deep nested logic: static analyzers will flag high complexity
        if value:
            if value.isdigit():
                if int(value) > 10:
                    if int(value) < 100:
                        if int(value) % 2 == 0:
                            if int(value) % 3 == 0:
                                if int(value) % 5 == 0:
                                    return Response({"msg": "Highly divisible"})
                                else:
                                    return Response({"msg": "Divisible by 6"})
                            else:
                                return Response({"msg": "Even value"})
                        else:
                            return Response({"msg": "Odd value"})
                    else:
                        return Response({"msg": "Big number"})
                else:
                    return Response({"msg": "Small number"})
            else:
                return Response({"msg": "Not a number"})
        else:
            return Response({"msg": "Missing value"})
        
# ===============================================================
# 3. DEAD CODE BLOCKS / UNREACHABLE CODE
# ===============================================================

class DeadCodeAPI(APIView):
    def get(self, request):

        return Response({"msg": "This will return first"})

        unreachable_var = "this code is dead"  # Dead code (never executed)
        print("This will never execute")      
        return Response({"msg": unreachable_var})

    def unused_function(self):  # Entire function is dead code
        x = 1
        y = 2
        return x + y
    
# ===============================================================
# 4. REDUNDANT / DUPLICATE CODE
# ===============================================================

class DuplicateCodeAPI(APIView):
    def get(self, request):
        # Repeated logic
        name = request.GET.get("name", "")
        if name == "test":
            msg = "Hello Test"
        else:
            msg = "Hello User"

        # Duplicate block
        if name == "test":
            msg2 = "Hello Test"
        else:
            msg2 = "Hello User"

        return Response({"msg1": msg, "msg2": msg2})
    

# ===============================================================
# 5. READABILITY ISSUES (long lines, no formatting, messy code)
# ===============================================================

class BadReadabilityAPI(APIView):
    def get(self,request):
        longLine="this is a very very very long line concatenated"+"without proper formatting and codacy will definitely catch this because the code is extremely unreadable"+str(123456789)
        return Response({"data":longLine})
    
# ===============================================================
# 6. HARDCODED CREDENTIALS (security risk)
# ===============================================================

class HardcodedSecretsAPI(APIView):
    def get(self, request):
        SECRET_KEY = "AKIAIOSFODNN7EXAMPLE"   # Hardcoded AWS key
        PASSWORD = "P@ssw0rd123"             # Hardcoded password
        API_TOKEN = "12345-ABCDE-TOKEN"      # Hardcoded access token

        return Response({"msg": "Bad secrets present"})
    

# ===============================================================
# 7. SECURITY VULNERABILITIES (SQL injection, XSS, unsafe eval)
# ===============================================================

class SecurityIssueAPI(APIView):
    def get(self, request):
        user_input = request.GET.get("name")

        # SQL Injection vulnerability
        query = f"SELECT * FROM auth_user WHERE username = '{user_input}'"
        with connection.cursor() as cursor:
            cursor.execute(query)   # UNSAFE
            result = cursor.fetchall()

        # Unsafe eval
        try:
            dangerous = eval(user_input)    
        except:
            dangerous = "error"

        # XSS Vulnerability
        html = f"<h1>Hello {user_input}</h1>"  # No sanitization

        return Response({"sql": result, "eval": dangerous, "html": html})


# ===============================================================
# 8. PERFORMANCE BOTTLENECK
# ===============================================================

from .models import Employee

class PerformanceIssueAPI(APIView):
    def get(self, request):

        # N+1 query
        data = []
        employees = Employee.objects.all()
        for emp in employees:
            data.append({
                "id": emp.id,
                "name": emp.name,
                "extra": Employee.objects.get(id=emp.id).name  # BAD — extra query inside loop
            })

        # Inefficient loop
        large = 0
        for i in range(0, 9000000):   # Very large loop — performance
            large += i

        return Response({"count": len(data)})

# ===============================================================
# 9. BAD ERROR HANDLING
# ===============================================================

class BadErrorHandlingAPI(APIView):
    def get(self, request):
        try:
            x = 1 / 0
        except Exception:    # Broad exception
            pass             # Swallowing exception

        return Response({"msg": "Bad error handling"})

# ===============================================================
# 10. TIGHTLY COUPLED CODE (no separation of concerns)
# ===============================================================

class TightlyCoupledAPI(APIView):
    def get(self, request):

        # Direct DB interaction + business logic + formatting mixed together
        # Codacy will suggest modularization
        employees = Employee.objects.all()

        data = []
        for emp in employees:
            if emp.salary > 1000:
                if emp.salary < 3000:
                    if emp.department == "IT":
                        data.append({"id": emp.id, "name": emp.name, "salary": emp.salary})

        return Response({"data": data})







