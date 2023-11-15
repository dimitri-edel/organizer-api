""" Function based api views
    There is a bug in dj-rest-auth that will not logout the user
    when JWT is enabled. The logout method needs to be
    declared manually to fix the problem
 """
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .settings import (
    JWT_AUTH_COOKIE,
    JWT_AUTH_REFRESH_COOKIE,
    JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)

# pylint: disable=W0613


@api_view()
def root_route(request):
    """Return a welcome message at the root URL"""
    return Response({"message": "Welcome to ORGANIZER-API !"})


@api_view(["POST"])
def logout_route(request):
    """dj-rest-auth logout view Bug Fix"""
    response = Response()
    response.set_cookie(
        key=JWT_AUTH_COOKIE,
        value="",
        httponly=True,
        expires="Thu, 01 Jan 1970 00:00:00 GMT",
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    response.set_cookie(
        key=JWT_AUTH_REFRESH_COOKIE,
        value="",
        httponly=True,
        expires="Thu, 01 Jan 1970 00:00:00 GMT",
        max_age=0,
        samesite=JWT_AUTH_SAMESITE,
        secure=JWT_AUTH_SECURE,
    )
    return response
