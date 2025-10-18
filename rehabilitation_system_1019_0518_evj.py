# 代码生成时间: 2025-10-19 05:18:47
from django.db import models
from django.shortcuts import render, redirect
from django.urls import path
from django.http import HttpResponse, Http404
from django.views import View
from django.views.decorators.http import require_http_methods

# Define models for the Rehabilitation System
class Patient(models.Model):
    """Model to store patient information"""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    condition = models.TextField()
    treatment_plan = models.TextField(blank=True, null=True)

    def __str__(self):  # String representation of the Patient
        return f"{self.first_name} {self.last_name}"

# Define views for the Rehabilitation System
class PatientListView(View):
    """View to display a list of all patients."""
    def get(self, request):  # GET request method
        try:  # Error handling for retrieving patients
            patients = Patient.objects.all()
        except Exception as e:  # Generic exception catch
            return HttpResponse(f"An error occurred: {str(e)}", status=500)
        return render(request, 'patients/list.html', {'patients': patients})

class PatientDetailView(View):
    """View to display a detailed view of a single patient."""
    def get(self, request, patient_id):  # GET request method with patient ID
        try:  # Error handling for retrieving a specific patient
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:  # Specific exception for not found
            raise Http404("Patient not found.")
        except Exception as e:  # Generic exception catch
            return HttpResponse(f"An error occurred: {str(e)}", status=500)
        return render(request, 'patients/detail.html', {'patient': patient})

# Define URLs for the Rehabilitation System
urlpatterns = [  # List of URL patterns
    path('patients/', PatientListView.as_view(), name='patient-list'),  # URL for patient list
    path('patients/<int:patient_id>/', PatientDetailView.as_view(), name='patient-detail'),  # URL for patient detail
]

# Note: You would need to create the corresponding templates (e.g., patients/list.html and patients/detail.html) to display the information.
