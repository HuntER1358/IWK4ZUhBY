# 代码生成时间: 2025-10-07 19:03:48
from django.conf import settings
from django.contrib.auth.models import User
# TODO: 优化性能
from django.db import models
from django.utils import timezone
from django.urls import path
from django.http import JsonResponse
# NOTE: 重要实现细节
from django.views import View
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_payload_handler
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework import status
import jwt


class JWTToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jwt_token')
    token = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.user.username


class JWTManager:
    """
    JWTManager class handles JWT token generation and validation.
    It also includes methods to create, update, and delete tokens.
    """

    @staticmethod
    def create_token(user):
        """
        Create a new JWT token for the user.
        :param user: User instance
        :return: JWT token string
        """
# NOTE: 重要实现细节
        payload = jwt_payload_handler(user)
        payload['user_id'] = user.id
        payload['exp'] = timezone.now() + api_settings.JWT_EXPIRATION_DELTA
# FIXME: 处理边界情况
        token = jwt.encode(payload, api_settings.SECRET_KEY, algorithm=api_settings.JWT_ALGORITHM)
        return token
# FIXME: 处理边界情况

    @staticmethod
# NOTE: 重要实现细节
    def get_user_by_token(token):
# FIXME: 处理边界情况
        """
        Retrieve user instance by JWT token.
        :param token: JWT token string
        :return: User instance or None
        """
# 扩展功能模块
        try:
            payload = jwt.decode(token, api_settings.SECRET_KEY, algorithms=[api_settings.JWT_ALGORITHM])
            user = User.objects.get(id=payload['user_id'])
            return user
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
# 添加错误处理
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def verify_token(token):
        """
        Verify the JWT token.
        :param token: JWT token string
# 增强安全性
        :return: None or raises exception
        """
# NOTE: 重要实现细节
        try:
            jwt.decode(token, api_settings.SECRET_KEY, algorithms=[api_settings.JWT_ALGORITHM])
        except jwt.ExpiredSignatureError:
            raise Exception('Token has expired')
        except jwt.InvalidTokenError:
            raise Exception('Invalid token')
# NOTE: 重要实现细节


class TokenCreateView(ObtainJSONWebToken):
# NOTE: 重要实现细节
    """
    View to create a new JWT token.
    """
    pass


class TokenRefreshView(View):
    """
    View to refresh an existing JWT token.
    """
    def post(self, request, *args, **kwargs):
        token = request.data.get('refresh')
        if not token:
            return JsonResponse({'error': 'Refresh token not provided'}, status=status.HTTP_400_BAD_REQUEST)
# TODO: 优化性能
        try:
# TODO: 优化性能
            payload = jwt.decode(token, api_settings.SECRET_KEY,
# NOTE: 重要实现细节
                                 algorithms=[api_settings.JWT_ALGORITHM])
            new_token = JWTManager.create_token(paylaod['user'])
            return JsonResponse({'new_token': new_token})
        except jwt.ExpiredSignatureError:
            return JsonResponse({'error': 'Refresh token has expired'},
                                 status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return JsonResponse({'error': 'Invalid refresh token'},
                                 status=status.HTTP_401_UNAUTHORIZED)


urlpatterns = [
    # Define your URL patterns here
    path('api-token-auth/', TokenCreateView.as_view(), name='api_token_auth'),
    path('api-token-refresh/', TokenRefreshView.as_view(), name='api_token_refresh'),
]
# NOTE: 重要实现细节
