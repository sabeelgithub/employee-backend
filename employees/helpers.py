from rest_framework import status

from utils import custom_response

def employee_create_success(data):
    return custom_response(
        message="Employee Created Successfully",
        status=status.HTTP_200_OK,
        data=data
    )

def employee_update_success():
    return custom_response(
        message="Employee Updated Successfully",
        status=status.HTTP_200_OK
    )

def employee_not_found():
    return custom_response(
        message="Employee Not Found",
        status=status.HTTP_404_NOT_FOUND
    )

def employee_success_list(data):
    return custom_response(
        message="Employee List",
        status=status.HTTP_200_OK,
        data=data
    )

def employee_delete_success():
    return custom_response(
        message="Employee Deleted Successfully",
        status=status.HTTP_200_OK
    )

def employee_detail_success(data):
    return custom_response(
        message="Employee Details",
        status=status.HTTP_200_OK,
        data=data
    )
