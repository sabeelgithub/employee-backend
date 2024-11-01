from rest_framework import status

from utils import custom_response
def username_already_exists():
    return custom_response(
        message="Username Already Exists",
        status=status.HTTP_409_CONFLICT
    )

def email_already_exists():
    return custom_response(
        message="Email Already Exists",
        status=status.HTTP_409_CONFLICT
    )

def phone_already_exists():
    return custom_response(
        message="Phone Already Exists",
        status=status.HTTP_409_CONFLICT
    )

def password_length_issue():
    return custom_response(
        message="Password must be at least 5 characters long",
        status=status.HTTP_400_BAD_REQUEST
    )

def user_create_success(data):
    return custom_response(
        message="User created successfully",
        status=status.HTTP_201_CREATED,
        data=data
    )
