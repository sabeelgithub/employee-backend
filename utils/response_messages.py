from rest_framework import status

def custom_response(message,status,data=None):
    return {
        "message":message,
        "status":status,
        "data":data
    }

def custom_error_response(message,status,error=None):
    return {
        "message":message,
        "status":status,
        "error":error
    }


def internal_server_error_response(e):
    return custom_error_response(
        message=f"Something Went Wrong With {str(e)}",
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

def invalid_inputs(error):
    return custom_error_response(
        message="Invalid input. Please review and correct your form entries",
        status=status.HTTP_400_BAD_REQUEST,
        error=error

    )