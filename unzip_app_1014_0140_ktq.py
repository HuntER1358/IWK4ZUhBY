# 代码生成时间: 2025-10-14 01:40:25
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse, JsonResponse
from django.conf import settings
import zipfile
import shutil
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render
from django.core.exceptions import ValidationError
import os
import tempfile

"""
A Django application component for decompressing files.
"""
class FileDecompressor(View):
    """
    View to handle file decompression.
    """

    @method_decorator(require_http_methods(['POST']), name='dispatch')
    def post(self, request):
        """
        Handle file uploads and decompression.
        """
        # Check if the request contains a file
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file provided.'}, status=400)
        
        uploaded_file = request.FILES['file']
        
        # Check if the file is a zip file
        if not uploaded_file.name.endswith('.zip'):
            return JsonResponse({'error': 'Unsupported file type. Only .zip files are allowed.'}, status=400)
        
        try:
            # Create a temporary directory to extract the file
            with tempfile.TemporaryDirectory() as temp_dir:
                zip_path = os.path.join(temp_dir, uploaded_file.name)
                
                # Save the uploaded file to the temporary directory
                with open(zip_path, 'wb+') as f:
                    for chunk in uploaded_file.chunks():
                        f.write(chunk)
                
                # Extract the zip file
                with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                
                # Return the path of the extracted files
                extracted_files = []
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        extracted_files.append(file_path)
                
                return JsonResponse({'extracted_files': extracted_files})
        except zipfile.BadZipFile:
            return JsonResponse({'error': 'Invalid zip file.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
"""
URLs for the decompression app.
"""
from django.urls import path
from .views import FileDecompressor

urlpatterns = [
    path('decompress/', FileDecompressor.as_view(), name='decompress'),
]

"""
Models for the decompression app.
"""
from django.db import models

class DecompressedFile(models.Model):
    """
    Model to store information about decompressed files.
    """
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=1024)
    
    def __str__(self):
        return self.name