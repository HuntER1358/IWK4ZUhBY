# 代码生成时间: 2025-10-17 03:38:26
import os
import psutil
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.urls import path
from django.http import JsonResponse, HttpResponse
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from .forms import ProcessForm
"""
进程管理器应用，提供进程列表查看和进程操作功能
"""
class Process(models.Model):
    pid = models.IntegerField(verbose_name="进程ID")
    name = models.CharField(max_length=100, verbose_name="进程名称")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "进程"
        verbose_name_plural = "进程"

class ProcessListView(ListView):
    """
    进程列表视图，返回所有进程的列表
    """
    model = Process
    template_name = 'process/process_list.html'
    context_object_name = 'process_list'

    def get_queryset(self):
        """
        获取进程列表
        """
        return Process.objects.all()

class ProcessDetailView(DetailView):
    """
    进程详细信息视图，返回指定进程的详细信息
    """
    model = Process
    template_name = 'process/process_detail.html'
    context_object_name = 'process'

    def get_queryset(self):
        """
        获取进程列表
        """
        return Process.objects.all()

@csrf_exempt  # 禁用CSRF验证
def process_list(request):
    """
    进程列表接口，返回所有进程信息
    """
    processes = []
    for proc in psutil.process_iter(['pid', 'name']):
        process = {
            'pid': proc.info['pid'],
            'name': proc.info['name']
        }
        processes.append(process)
    if request.method == 'GET':
        return JsonResponse({'code': 200, 'data': processes})
    return HttpResponse('Method not allowed', status=405)

@csrf_exempt  # 禁用CSRF验证
def process_detail(request, pid):
    """
    进程详细信息接口，返回指定进程的详细信息
    """
    try:
        process = psutil.Process(int(pid))
        info = {
            'pid': process.pid,
            'name': process.name(),
            'create_time': process.create_time(),
            'status': process.status(),
            'memory_info': process.memory_info()._asdict()
        }
        if request.method == 'GET':
            return JsonResponse({'code': 200, 'data': info})
    except psutil.NoSuchProcess:
        return JsonResponse({'code': 404, 'msg': 'Process not found'}, status=404)
    except Exception as e:
        return JsonResponse({'code': 500, 'msg': str(e)}, status=500)
    return HttpResponse('Method not allowed', status=405)

# urls配置
urlpatterns = [
    path('process_list/', process_list, name='process_list'),
    path('process_detail/<int:pid>/', process_detail, name='process_detail')
]
