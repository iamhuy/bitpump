from rest_framework.exceptions import APIException, NotFound
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler
from rest_framework.exceptions import NotAuthenticated


def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        if isinstance(exc, NotAuthenticated):
            response.data = {'detail': 'You need to login to view this content. Please Login.'}
            response.status_code = status.HTTP_401_UNAUTHORIZED
        try:
            response.data['error'] = exc.error_code
        except AttributeError:
            response.data['error'] = 1
    else:
        response = Response({'error': 1, 'detail': 'System Error'})
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    return response


class SystemErrorException(APIException):
    status_code = status.HTTP_200_OK
    error_code = 1
    default_detail = "System Error"


class DuplicateUserEmailException(APIException):
    error_code = 2
    default_detail = 'User email is duplicate'


class ObjectNotFoundException(APIException):
    error_code = 3
    default_detail = 'Object not found'


class InputIsInvalidException(SystemErrorException):
    error_code = 4
    default_detail = 'Input parameters are invalid'


class LocationVerifyFailException(SystemErrorException):
    error_code = 5
    default_detail = 'Location verify fail'


class ImageVerifyFailException(SystemErrorException):
    error_code = 6
    default_detail = 'Image verify fail'
