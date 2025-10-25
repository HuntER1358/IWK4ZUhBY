# 代码生成时间: 2025-10-25 22:09:08
import json
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
from .models import Item

"""
RESTful API component for the 'items' resource.
Provides CRUD operations to interact with the 'Item' model.
"""


class ItemAPI:
    """
    A class-based view handling RESTful API requests for the 'Item' resource.
    """

    @require_http_methods(['GET', 'POST'])
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        """
        List all items.
        """
        items = Item.objects.all()
        return JsonResponse(list(map(lambda item: item.to_dict(), items)), safe=False)

    def post(self, request):
        """
        Create a new item.
        """
        data = json.loads(request.body)
        try:
            item = Item.objects.create(**data)
            return JsonResponse(item.to_dict())
        except TypeError as e:
            return JsonResponse({'error': str(e)}, status=400)

    def put(self, request, pk):
        """
        Update an existing item.
        """
        data = json.loads(request.body)
        try:
            item = Item.objects.get(pk=pk)
            for key, value in data.items():
                setattr(item, key, value)
            item.save()
            return JsonResponse(item.to_dict())
        except ObjectDoesNotExist:
            raise Http404
        except TypeError as e:
            return JsonResponse({'error': str(e)}, status=400)

    def delete(self, request, pk):
        """
        Delete an item.
        """
        try:
            item = Item.objects.get(pk=pk)
            item.delete()
            return JsonResponse({'success': True})
        except ObjectDoesNotExist:
            raise Http404


# Assuming a corresponding model Item
from django.db import models

class Item(models.Model):
    """
    A simple item model for demonstration purposes.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def to_dict(self):
        """
        Serialize the item instance to a dictionary.
        """
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description
        }

# urls.py
from django.urls import path
from .views import ItemAPI

urlpatterns = [
    path('items/', ItemAPI.as_view(), name='items'),
    path('items/<int:pk>/', ItemAPI.as_view(), name='item-detail'),
]
