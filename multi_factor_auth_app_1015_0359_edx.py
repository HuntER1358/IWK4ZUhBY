# 代码生成时间: 2025-10-15 03:59:22
# multi_factor_auth_app
# Django application for multi-factor authentication.

"""
This Django app provides multi-factor authentication functionality.
It includes models for storing authentication data, views for handling authentication
requests, and URL configurations for routing.
"""

# models.py
"""
Models for the multi-factor authentication app.
"""
from django.db import models
from django.contrib.auth.models import User

class MFADevice(models.Model):
    """Model representing a multi-factor authentication device."""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    device_name = models.CharField(max_length=100)
    secret_key = models.CharField(max_length=255)  # TOTP secret key

    def __str__(self):
        return f"{self.user.username}'s {self.device_name}"

class MFAToken(models.Model):
    """Model representing a multi-factor authentication token."""
    device = models.ForeignKey(MFADevice, on_delete=models.CASCADE)
    token = models.CharField(max_length=6)  # 6-digit token
    created_at = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)

    def __str__(self):
        return f"Token for {self.device.device_name} at {self.created_at}"

# views.py
"""
Views for the multi-factor authentication app.
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .models import MFADevice, MFAToken
from django.contrib.auth.decorators import login_required
from pyotp import TOTP
import logging

logger = logging.getLogger(__name__)

@login_required
def verify_mfa(request):
    """
    View to verify the multi-factor authentication token.
    Returns a JSON response indicating whether the token is valid or not.
    """
    user = request.user
    device = MFADevice.objects.get(user=user)
    
    token = request.POST.get('token')
    if not token:
        return JsonResponse({'error': 'Token is required.'}, status=400)
    
    totp = TOTP(device.secret_key)
    if totp.verify(token):
        # Create and save a new MFAToken instance
        MFAToken.objects.create(device=device, token=token)
        return JsonResponse({'success': 'MFA token is valid.'})
    else:
        logger.error(f"Invalid MFA token for user {user.username}")
        return JsonResponse({'error': 'Invalid MFA token.'}, status=401)

# urls.py
"""
URL configurations for the multi-factor authentication app.
"""
from django.urls import path
from .views import verify_mfa

urlpatterns = [
    path('verify/', verify_mfa, name='verify_mfa'),
]
