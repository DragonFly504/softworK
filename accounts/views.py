from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import UserProfile
import json
from datetime import datetime


@csrf_exempt
@require_http_methods(["POST"])
def login_view(request):
    """Login endpoint - authenticates user and creates session"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        if not email or not password:
            return JsonResponse({"message": "Email and password are required"}, status=400)
        
        # Try to find user by email (Django uses username by default)
        try:
            user = User.objects.get(email=email)
            username = user.username
        except User.DoesNotExist:
            # Also try email as username
            username = email
        
        # Authenticate
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                "success": True,
                "message": "Login successful",
                "redirect": "/profile/",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                }
            })
        else:
            return JsonResponse({"success": False, "message": "Invalid email or password"}, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def register_view(request):
    """Register endpoint - creates new user account"""
    try:
        data = json.loads(request.body)
        
        # Extract fields
        email = data.get('email', '').strip()
        password = data.get('password', '')
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        phone = data.get('phone', '').strip()
        dob = data.get('dob', '').strip()
        ssn = data.get('ssn', '').strip()
        address = data.get('address', '').strip()
        city = data.get('city', '').strip()
        state = data.get('state', '').strip()
        zipcode = data.get('zipcode', '').strip()
        country = data.get('country', 'US').strip()
        
        # Validation
        if not email:
            return JsonResponse({"success": False, "message": "Email is required"}, status=400)
        if not password:
            return JsonResponse({"success": False, "message": "Password is required"}, status=400)
        if len(password) < 8:
            return JsonResponse({"success": False, "message": "Password must be at least 8 characters"}, status=400)
        if not first_name or not last_name:
            return JsonResponse({"success": False, "message": "First name and last name are required"}, status=400)
        if not dob:
            return JsonResponse({"success": False, "message": "Date of birth is required"}, status=400)
        if not ssn:
            return JsonResponse({"success": False, "message": "SSN is required"}, status=400)
        
        # Validate SSN format
        ssn_clean = ssn.replace('-', '')
        if len(ssn_clean) != 9 or not ssn_clean.isdigit():
            return JsonResponse({"success": False, "message": "Invalid SSN format"}, status=400)
        
        # Format SSN consistently
        ssn_formatted = f"{ssn_clean[:3]}-{ssn_clean[3:5]}-{ssn_clean[5:]}"
        
        # Validate age (must be 18+)
        try:
            birth_date = datetime.strptime(dob, '%Y-%m-%d').date()
            today = datetime.now().date()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            if age < 18:
                return JsonResponse({"success": False, "message": "You must be at least 18 years old"}, status=400)
        except ValueError:
            return JsonResponse({"success": False, "message": "Invalid date of birth format"}, status=400)
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return JsonResponse({"success": False, "message": "An account with this email already exists"}, status=400)
        if User.objects.filter(username=email).exists():
            return JsonResponse({"success": False, "message": "An account with this email already exists"}, status=400)
        
        # Create user (use email as username)
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        
        # Create user profile with additional fields
        UserProfile.objects.create(
            user=user,
            phone=phone,
            date_of_birth=birth_date,
            ssn=ssn_formatted,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            country=country,
        )
        
        return JsonResponse({
            "success": True,
            "message": "Account created successfully",
            "redirect": "/signin",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"message": str(e)}, status=500)


def logout_view(request):
    """Logout endpoint - ends user session"""
    logout(request)
    return redirect('home')


def forgot_password_page(request):
    """Render the forgot password page"""
    return render(request, 'forgot_password.html')


@csrf_exempt
@require_http_methods(["POST"])
def forgot_password_view(request):
    """Handle forgot password request - sends reset email"""
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip()
        
        if not email:
            return JsonResponse({"success": False, "message": "Email is required"}, status=400)
        
        # Check if user exists
        try:
            user = User.objects.get(email=email)
            # In a production environment, you would:
            # 1. Generate a password reset token
            # 2. Send an email with the reset link
            # For now, we'll just acknowledge the request
            # This prevents email enumeration attacks
        except User.DoesNotExist:
            pass  # Don't reveal if email exists or not
        
        # Always return success to prevent email enumeration
        return JsonResponse({
            "success": True,
            "message": "If an account exists with this email, you will receive a password reset link."
        })
        
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


def profile_view(request):
    """User profile endpoint"""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "Not authenticated"}, status=401)
    
    user = request.user
    profile_data = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }
    
    # Add profile data if exists
    try:
        profile = user.profile
        profile_data.update({
            "phone": profile.phone,
            "date_of_birth": str(profile.date_of_birth) if profile.date_of_birth else None,
            "ssn_masked": profile.get_masked_ssn(),
            "address": profile.address,
            "city": profile.city,
            "state": profile.state,
            "zipcode": profile.zipcode,
            "country": profile.country,
            "full_address": profile.get_full_address(),
        })
    except UserProfile.DoesNotExist:
        pass
    
    return JsonResponse(profile_data)


def profile_page(request):
    """Render the profile page"""
    return render(request, 'profile.html')


@csrf_exempt
@require_http_methods(["POST"])
def profile_update_view(request):
    """Update user profile information"""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "Not authenticated"}, status=401)
    
    try:
        data = json.loads(request.body)
        user = request.user
        
        # Update user fields if provided
        if 'first_name' in data:
            user.first_name = data['first_name'].strip()
        if 'last_name' in data:
            user.last_name = data['last_name'].strip()
        user.save()
        
        # Get or create profile
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        # Update profile fields if provided
        if 'phone' in data:
            profile.phone = data['phone'].strip()
        if 'address' in data:
            profile.address = data['address'].strip()
        if 'city' in data:
            profile.city = data['city'].strip()
        if 'state' in data:
            profile.state = data['state'].strip()
        if 'zipcode' in data:
            profile.zipcode = data['zipcode'].strip()
        if 'country' in data:
            profile.country = data['country'].strip()
        
        profile.save()
        
        return JsonResponse({
            "success": True,
            "message": "Profile updated successfully"
        })
        
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def change_password_view(request):
    """Change user password"""
    if not request.user.is_authenticated:
        return JsonResponse({"success": False, "message": "Not authenticated"}, status=401)
    
    try:
        data = json.loads(request.body)
        current_password = data.get('current_password', '')
        new_password = data.get('new_password', '')
        
        if not current_password or not new_password:
            return JsonResponse({"success": False, "message": "Both passwords are required"}, status=400)
        
        if len(new_password) < 8:
            return JsonResponse({"success": False, "message": "New password must be at least 8 characters"}, status=400)
        
        user = request.user
        
        # Verify current password
        if not user.check_password(current_password):
            return JsonResponse({"success": False, "message": "Current password is incorrect"}, status=400)
        
        # Set new password
        user.set_password(new_password)
        user.save()
        
        # Re-login user to maintain session
        login(request, user)
        
        return JsonResponse({
            "success": True,
            "message": "Password changed successfully"
        })
        
    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)}, status=500)

