# 代码生成时间: 2025-10-25 06:49:52
# excel_generator_app/

# excel_generator_app/models.py
"""
Models for Excel Generator app.
"""
from django.db import models


class Data(models.Model):
    """
    A simple model to store data that will be used to generate an Excel file.
    """
    name = models.CharField(max_length=255)
    age = models.IntegerField()
    city = models.CharField(max_length=255)

    def __str__(self):
        return self.name


# excel_generator_app/views.py
"""
Views for Excel Generator app.
"""
import csv
from django.http import HttpResponse
from django.shortcuts import render
from .models import Data
from django.views import View
from django.core.exceptions import ObjectDoesNotExist

class ExcelGenerator(View):
    """
    A view to generate and return an Excel file with data from the Data model.
    """
    def get(self, request, *args, **kwargs):
        try:
            data_records = Data.objects.all().values('name', 'age', 'city')
            # Create a HttpResponse object with the appropriate CSV header.
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="data.csv"'
            writer = csv.writer(response)
            writer.writerow(['Name', 'Age', 'City'])
            for record in data_records:
                writer.writerow([record['name'], record['age'], record['city']])
            return response
        except ObjectDoesNotExist:
            return HttpResponse("No data found.", status=404)


# excel_generator_app/urls.py
"""
URLs for Excel Generator app.
"""
from django.urls import path
from .views import ExcelGenerator

urlpatterns = [
    path('generate-excel/', ExcelGenerator.as_view(), name='generate-excel'),
]

# excel_generator_app/admin.py
"""
Django admin configuration for Excel Generator app.
"""
from django.contrib import admin
from .models import Data

admin.site.register(Data)

# excel_generator_app/apps.py
"""
App configuration for Excel Generator app.
"""
from django.apps import AppConfig

class ExcelGeneratorAppConfig(AppConfig):
    name = 'excel_generator_app'
    verbose_name = 'Excel Generator'

    def ready(self):
        # Ready method to include any signal processors.
        pass
