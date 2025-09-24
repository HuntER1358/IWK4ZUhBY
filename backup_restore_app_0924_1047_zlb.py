# 代码生成时间: 2025-09-24 10:47:56
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core.management import call_command
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import os
import shutil
import logging

# 设置日志记录器
logger = logging.getLogger(__name__)

class BackupDatabaseView(View):
    """
    数据库备份视图
    """
    def post(self, request):
        """
        执行数据库备份
        """
        try:
            backup_name = f"db_backup_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.sql"
            with open(backup_name, 'w') as backup_file:
                call_command('dumpdb', stdout=backup_file)
            return JsonResponse({'status': 'success', 'message': 'Database backup created successfully.', 'filename': backup_name})
        except Exception as e:
            logger.error(f'Error during database backup: {e}')
            return JsonResponse({'status': 'error', 'message': str(e)})

class RestoreDatabaseView(View):
    """
    数据库恢复视图
    """
    def post(self, request):
        """
        执行数据库恢复
        """
        try:
            backup_file = request.FILES.get('backup_file')
            if not backup_file:
                return JsonResponse({'status': 'error', 'message': 'No backup file provided.'})
            with open(backup_file.name, 'wb') as file:
                for chunk in backup_file.chunks():
                    file.write(chunk)
            call_command('loaddata', backup_file.name)
            os.remove(backup_file.name)
            return JsonResponse({'status': 'success', 'message': 'Database restored successfully.'})
        except Exception as e:
            logger.error(f'Error during database restore: {e}')
            return JsonResponse({'status': 'error', 'message': str(e)})

# URLs
from django.urls import path
urlpatterns = [
    path('backup/', method_decorator(csrf_exempt)(BackupDatabaseView.as_view()), name='backup_database'),
    path('restore/', method_decorator(csrf_exempt)(RestoreDatabaseView.as_view()), name='restore_database'),
]
