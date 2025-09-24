# 代码生成时间: 2025-09-24 19:30:17
from django.db import models
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.utils.html import escape
from django.urls import path

"""
XSS Protection Application
=====================================
This Django app provides a basic model for data storage and
views to handle requests, enforcing XSS protection.
"""

class ProtectedData(models.Model):
    """
    A model to store data that could potentially be exposed to XSS attacks.
    It ensures data is escaped before being saved to prevent XSS.
    """
    content = models.TextField(help_text='Content to be stored with XSS protection.')

    def save(self, *args, **kwargs):
        """
        Override the save method to escape content before saving to the database.
        """
        self.content = escape(self.content)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.content


@require_http_methods(["GET", "POST"])
def data_view(request):
    """
    View to handle data submission and display, ensuring all content is escaped
    to prevent XSS attacks.
    
    Parameters:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: A response with the escaped content.
    """
    if request.method == "POST":
        # Retrieve and escape content from POST request
        content = escape(request.POST.get('content', ''))
        # Save the escaped content to the database
        protected_data = ProtectedData(content=content)
        protected_data.save()
        return HttpResponse(f"Content saved: {content}")
    else:
        # Retrieve all data from the database and escape it before displaying
        data_list = ProtectedData.objects.all().values_list('content', flat=True)
        escaped_content = "
".join([escape(content) for content in data_list])
        return HttpResponse(escaped_content)

# URL configuration for the XSS protection view
urlpatterns = [
    path("data/", data_view, name="xss_protection")
]