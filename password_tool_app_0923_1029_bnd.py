# 代码生成时间: 2025-09-23 10:29:13
# password_tool_app/password_tool_app
"""
Password Encryption and Decryption Tool
This Django app provides functionality for encrypting and decrypting passwords.
"""
from django.apps import AppConfig

class PasswordToolAppConfig(AppConfig):
    name = 'password_tool_app'
    verbose_name = 'Password Tool Application'

# password_tool_app/models.py
"""
Models for Password Tool Application
"""
from django.db import models
from django.utils.translation import gettext_lazy as _

class PasswordModel(models.Model):
    """
    Model to store encrypted passwords.
    """
    encrypted_password = models.CharField(_('encrypted password'), max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Encrypted Password {self.id}"

# password_tool_app/views.py
"""
Views for Password Tool Application
"""
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from django.views import View
from .models import PasswordModel
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from cryptography.fernet import Fernet, InvalidToken

class EncryptionDecryptionView(View):
    """
    View to handle password encryption and decryption.
    """
    def get(self, request, *args, **kwargs):
        """
        GET request to return documentation of the API.
        """
        return JsonResponse({'message': 'Use POST request to encrypt or decrypt passwords.'})
    
    @method_decorator(require_http_methods(['POST']), name='dispatch')
    def post(self, request, *args, **kwargs):
        """
        POST request to encrypt or decrypt passwords.
        """
        data = request.POST
        action = data.get('action')
        password = data.get('password')

        if not password:
            return JsonResponse({'error': 'Password is required.'}, status=400)

        if action == 'encrypt':
            return self.encrypt_password(password)
        elif action == 'decrypt':
            return self.decrypt_password(password)
        else:
            return JsonResponse({'error': 'Invalid action.'}, status=400)

    def encrypt_password(self, password):
        """
        Encrypt the provided password.
        """
        key = Fernet.generate_key()
        cipher_suite = Fernet(key)
        encrypted_password = cipher_suite.encrypt(force_bytes(password))

        try:
            decrypted_password = cipher_suite.decrypt(encrypted_password).decode()
            assert password == decrypted_password
            PasswordModel.objects.create(encrypted_password=encrypted_password)
        except (AssertionError, InvalidToken):
            return JsonResponse({'error': 'Encryption failed.'}, status=500)

        return JsonResponse({'encrypted': urlsafe_base64_encode(encrypted_password)})

    def decrypt_password(self, password):
        """
        Decrypt the provided password.
        """
        encrypted_password = urlsafe_base64_decode(password)
        try:
            cipher_suite = Fernet(Fernet.generate_key())
            decrypted_password = cipher_suite.decrypt(force_bytes(encrypted_password)).decode()
        except InvalidToken:
            return JsonResponse({'error': 'Decryption failed.'}, status=500)

        return JsonResponse({'decrypted': decrypted_password})

# password_tool_app/urls.py
"""
URLs for Password Tool Application
"""
from django.urls import path
from .views import EncryptionDecryptionView

urlpatterns = [
    path('encrypt-decrypt/', EncryptionDecryptionView.as_view(), name='encrypt-decrypt'),
]
