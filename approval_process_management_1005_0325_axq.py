# 代码生成时间: 2025-10-05 03:25:21
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


# Model for Approval Process
class ApprovalProcess(models.Model):
    """审批流程模型"""
    name = models.CharField(max_length=255, verbose_name="审批名称")
    description = models.TextField(blank=True, null=True, verbose_name="审批描述")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        return self.name

    # Validation to ensure name is unique
    def clean(self):
        if ApprovalProcess.objects.filter(name=self.name).exists():
            raise ValidationError("Approval process with this name already exists.")

    # Signal to perform actions after saving
    @receiver(post_save, sender=ApprovalProcess)
    def update_approval_process(sender, instance, created, **kwargs):
        if created:
            print(f"Approval process {instance.name} created.")
        else:
            print(f"Approval process {instance.name} updated.")


# View for handling Approval Process
class ApprovalProcessView(View):
    """视图处理审批流程"""
    @method_decorator(csrf_exempt, name='dispatch')
    def post(self, request, *args, **kwargs):
        """创建一个新的审批流程"""
        try:
            name = request.POST.get('name')
            description = request.POST.get('description')
            process = ApprovalProcess.objects.create(name=name, description=description)
            return JsonResponse({'message': 'Approval process created successfully.', 'id': process.id})
        except ValidationError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def get(self, request, *args, **kwargs):
        """获取所有审批流程列表"""
        try:
            processes = ApprovalProcess.objects.all()
            processes_data = [{'id': p.id, 'name': p.name, 'description': p.description} for p in processes]
            return JsonResponse({'data': processes_data})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# URL configuration for Approval Process
app_name = 'approval'
urlpatterns = [
    path('process/', ApprovalProcessView.as_view(), name='approval_process'),
]
