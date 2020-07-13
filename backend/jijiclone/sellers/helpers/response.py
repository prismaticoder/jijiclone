from rest_framework.response import Response
from rest_framework import status

def sendRes(data, status_code=False,custom_msg=None):

    return Response(
        {
            "status": status_code or 200, 
            "success": True,
            "message": custom_msg or "Query successful", 
            "data": data
        },
        status=status_code or status.HTTP_200_OK
    )

def sendError(status_code, custom_msg=None):

    if custom_msg:
        error_msg = custom_msg
    
    else:
        if status_code == 404:
            error_msg = "Resource Not Found"
        elif status_code == 500:
            error_msg = "Internal Server Error"
        elif status_code == 400:
            error_msg = "Invalid Request"
        elif status_code == 401:
                error_msg = "You are not authorized to make this request"
        elif status_code == 403:
            error_msg = "Access Forbidden"

    return Response(
        {
            "status": status_code, 
            "success": False,
            "error": error_msg,
        },
        status=status_code
    )