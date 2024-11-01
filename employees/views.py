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
            employees = Employee.objects.filter(*q_object).order_by('-created_at')
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