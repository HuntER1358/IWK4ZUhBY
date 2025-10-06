# 代码生成时间: 2025-10-07 03:03:20
from django.contrib import admin
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.urls import path
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import plot_model
import io
import base64

"""
Neural Network Visualizer Django Application
=====================================
This Django application provides a web interface to visualize neural networks.
"""

# Define a model for storing neural network data
class NeuralNetworkModel(models.Model):
    model_name = models.CharField(max_length=255)
    model_data = models.BinaryField()
    
    def __str__(self):
        return self.model_name

# Define a view to handle neural network visualization requests
class NeuralNetworkVisualizer(View):
    """
    A Django view to visualize neural networks.
    
    This view loads a neural network model from the database,
    generates a visualization, and returns it as an image.
    """
    def get(self, request, *args, **kwargs):
        try:
            # Load the neural network model from the database
            model_id = request.GET.get('model_id')
            if not model_id:
                return JsonResponse({'error': 'Model ID is required'}, status=400)
            model = NeuralNetworkModel.objects.get(id=model_id)
            model_data = model.model_data
            model = load_model(model_data)
            
            # Generate a visualization of the neural network
            buf = io.BytesIO()
            plot_model(model, to_file=buf, show_shapes=True, show_layer_names=True)
            buf.seek(0)
            
            # Convert the visualization to a base64-encoded image
            image_data = base64.b64encode(buf.read()).decode('utf-8')
            
            # Return the image data in the response
            return JsonResponse({'image_data': image_data}, status=200)
        except NeuralNetworkModel.DoesNotExist:
            return JsonResponse({'error': 'Model not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

# Define a URL pattern for the neural network visualizer view
urlpatterns = [
    path('visualize/', NeuralNetworkVisualizer.as_view(), name='visualize'),
]
