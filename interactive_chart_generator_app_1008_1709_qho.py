# 代码生成时间: 2025-10-08 17:09:54
# interactive_chart_generator_app/models.py
"""
This module defines the models used by the interactive chart generator.
"""
from django.db import models

# Define your models here.

class ChartData(models.Model):
    """Model to store chart data."""
    title = models.CharField(max_length=200)
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# interactive_chart_generator_app/views.py
"""
This module defines the views for the interactive chart generator.
"""
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from .models import ChartData
from .forms import ChartDataForm
import json

# Create your views here.

def chart_data_list(request):
    """
    List all chart data or create a new chart data entry.
    """
    if request.method == 'GET':
        chart_data_list = ChartData.objects.all()
        return render(request, 'chart_data_list.html', {'chart_data_list': chart_data_list})
    elif request.method == 'POST':
        form = ChartDataForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success', 'message': 'Chart data created successfully.'}, status=201)
        else:
            return JsonResponse({'status': 'error', 'message': 'Invalid form data.'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


# interactive_chart_generator_app/urls.py
"""
This module defines the URL patterns for the interactive chart generator.
"""
from django.urls import path
from .views import chart_data_list

# Define your URL patterns here.
urlpatterns = [
    path('charts/', chart_data_list, name='chart_data_list'),
]

# interactive_chart_generator_app/forms.py
"""
This module defines the forms used by the interactive chart generator.
"""
from django import forms
from .models import ChartData

class ChartDataForm(forms.ModelForm):
    """Form to create or update chart data."""
    class Meta:
        model = ChartData
        fields = ['title', 'data']

    def clean_data(self):
        """
        Ensure that the data field is a valid JSON string.
        """
        data = self.cleaned_data.get('data')
        try:
            json.loads(data)
        except json.JSONDecodeError:
            raise forms.ValidationError('Invalid JSON data.')
        return data


# interactive_chart_generator_app/admin.py
"""
This module defines the admin interface for the interactive chart generator.
"""
from django.contrib import admin
from .models import ChartData

# Register your models here.
@admin.register(ChartData)
class ChartDataAdapter(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)
    list_filter = ('created_at',)


# interactive_chart_generator_app/templates/chart_data_list.html
<!--
This template displays the list of chart data entries and provides a form to create a new entry.
-->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chart Data List</title>
</head>
<body>
    <h1>Chart Data List</h1>
    <a href="#" onclick="openModal('newChartDataModal')">Add New Chart Data</a>
    <div id="newChartDataModal" style="display:none;" class="modal">
        <form method="POST" action="{% url 'chart_data_list' %}">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Submit</button>
        </form>
    </div>
    <ul>
        {% for chart_data in chart_data_list %}
        <li>
            {{ chart_data.title }}
            <a href="#" onclick="openModal('editChartDataModal{{ forloop.counter0 }}')">Edit</a>
            <div id="editChartDataModal{{ forloop.counter0 }}" style="display:none;" class="modal">
                <form method="POST" action="{% url 'chart_data_list' %}">
                    {% csrf_token %}
                    {{ edit_form.as_p }}
                    <input type="hidden" name="id" value="{{ chart_data.id }}"/>
                    <button type="submit">Submit</button>
                </form>
            </div>
        </li>
        {% endfor %}
    </ul>
    <script>
        function openModal(modalId) {
            document.getElementById(modalId).style.display = 'block';
        }
    </script>
</body>
</html>