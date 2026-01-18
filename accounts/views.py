from django.shortcuts import render
from django.http import JsonResponse


def login_view(request):
    """Login endpoint"""
    return JsonResponse({"message": "Login endpoint"})


def register_view(request):
    """Register endpoint"""
    return JsonResponse({"message": "Register endpoint"})


def profile_view(request):
    """User profile endpoint"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not authenticated"}, status=401)
    return JsonResponse({
        "id": request.user.id,
        "username": request.user.username,
        "email": request.user.email,
    })
