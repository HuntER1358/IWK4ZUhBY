# 代码生成时间: 2025-10-05 22:16:46
import time
from django.db import models
from django.http import JsonResponse
from django.views import View
from django.urls import path
from django.core.exceptions import ValidationError
from locust import HttpUser, TaskSet, task, between
def generate_random_user_agent():
    """
    Generate a random user agent string for stress testing.
    """
    return "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"

class StressTestModel(models.Model):
    """
    Model to store stress test results.
    """
    test_id = models.AutoField(primary_key=True)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    success_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'stress_test_results'

    def __str__(self):
        return f"StressTestModel {self.test_id}"

class StressTestApp(UserTaskSet):
    """
    TaskSet class for Locust to perform stress testing.
    """
    def on_start(self):
        """
        On start of the task set.
        """
        self.client = self.environment.create_client()

    def on_stop(self):
        """
        On stop of the task set.
        """
        self.client.stop()

    @task
    def get_homepage(self):
        """
        A task to perform a GET request on the homepage.
        """
        with self.client.get("/", headers={"User-Agent": generate_random_user_agent()}) as response:
            response.success()

    @task
    def post_data(self):
        """
        A task to perform a POST request with data.
        """
        data = {"key": "value"}
        with self.client.post("/post", json=data, headers={"User-Agent": generate_random_user_agent()}) as response:
            response.success()

class StressTestView(View):
    """
    View to start and stop stress testing.
    """
    def get(self, request):
        """
        Get method to start stress testing.
        """
        try:
            test_id = StressTestModel.objects.create().test_id
            return JsonResponse({'test_id': test_id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    def post(self, request):
        """
        Post method to stop stress testing.
        """
        try:
            test_id = request.POST.get('test_id')
            test = StressTestModel.objects.get(test_id=test_id)
            test.end_time = time.time()
            test.success_count = request.POST.get('success_count', 0)
            test.error_count = request.POST.get('error_count', 0)
            test.save()
            return JsonResponse({'success': True})
        except StressTestModel.DoesNotExist:
            return JsonResponse({'error': 'Test not found'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

urlpatterns = [
    path('stress_test/start', StressTestView.as_view(), name='start_stress_test'),
    path('stress_test/stop', StressTestView.as_view(), name='stop_stress_test')
]
