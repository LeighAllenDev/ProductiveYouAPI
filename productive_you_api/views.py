from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .settings import (
    JWT_AUTH_COOKIE, JWT_AUTH_REFRESH_COOKIE, JWT_AUTH_SAMESITE,
    JWT_AUTH_SECURE,
)
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
@api_view(['POST'])
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        response = JsonResponse({'message': 'Login successful'})
        response.set_cookie(
            'my-app-auth', refresh.access_token, httponly=True,
            samesite='None', secure=request.is_secure()
        )
        response.set_cookie(
            'my-refresh-token', str(refresh), httponly=True,
            samesite='None', secure=request.is_secure()
        )
        return response
    return JsonResponse({'error': 'Invalid credentials'}, status=401)


@api_view(['GET'])
def root_route(request):
    return Response({
        "message": "Welcome to my ProductiveYou API for Code Institute PP05"
    })


@api_view(['POST'])
def logout_route(request):
    """
    Logs out the user by clearing the authentication and refresh token cookies.
    """
    response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    
    # Clear the authentication token cookie
    response.delete_cookie(
        key=settings.JWT_AUTH_COOKIE,
        samesite=settings.JWT_AUTH_SAMESITE,
        secure=settings.JWT_AUTH_SECURE,
    )
    
    # Clear the refresh token cookie
    response.delete_cookie(
        key=settings.JWT_AUTH_REFRESH_COOKIE,
        samesite=settings.JWT_AUTH_SAMESITE,
        secure=settings.JWT_AUTH_SECURE,
    )
    
    # Clear CSRF cookie if necessary
    response.delete_cookie('csrftoken')
    
    return response