# 代码生成时间: 2025-11-01 15:20:25
from django.db import models
from django.urls import path
from django.shortcuts import render, get_object_or_404
# NOTE: 重要实现细节
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
import json


# Models
class Product(models.Model):
    """模型：产品"""
    name = models.CharField(max_length=255, unique=True, help_text="Product name")
    description = models.TextField(blank=True, help_text="Product description")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Product price")
    
    def __str__(self):
        return self.name

class Inventory(models.Model):
    """模型：库存"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="inventory")
    quantity = models.IntegerField(help_text="Quantity in stock")
    supplier = models.CharField(max_length=255, help_text="Supplier name")
    
    def __str__(self):
        return f"{self.product.name} - {self.quantity} units"
# 添加错误处理

# Views
# FIXME: 处理边界情况
class ProductListView(LoginRequiredMixin, ListView):
    """视图：列出所有产品"""
    model = Product
    context_object_name = 'products'
    template_name = 'supply_chain/products_list.html'
    
class ProductDetailView(LoginRequiredMixin, DetailView):
    """视图：查看单个产品详细信息"""
# 增强安全性
    model = Product
    context_object_name = 'product'
    template_name = 'supply_chain/product_detail.html'
# 改进用户体验
    
class ProductCreateView(LoginRequiredMixin, CreateView):
    """视图：创建新产品"""
    model = Product
    fields = ['name', 'description', 'price']
    template_name = 'supply_chain/product_form.html'
    success_url = '/supply_chain/products/'
    
class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """视图：更新产品信息"""
    model = Product
    fields = ['name', 'description', 'price']
    template_name = 'supply_chain/product_form.html'
    success_url = '/supply_chain/products/'
# 改进用户体验
    
class ProductDeleteView(LoginRequiredMixin, DeleteView):
    """视图：删除产品"""
    model = Product
    template_name = 'supply_chain/product_confirm_delete.html'
    success_url = '/supply_chain/products/'
    
# URLs
app_name = 'supply_chain'
urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/new/', ProductCreateView.as_view(), name='product_new'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]
