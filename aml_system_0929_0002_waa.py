# 代码生成时间: 2025-09-29 00:02:21
# aml_system.py
"""Application module for Anti-Money Laundering (AML) system."""
from django.db import models
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
from django.urls import path

# Models
class Customer(models.Model):
    """Model representing a customer."""
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.TextField()
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    """Model representing a transaction."""
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Transaction {self.id} by {self.customer.name}"

    def clean(self):
        """Method to check for any suspicious activity."""
        if self.amount > 10000:  # Arbitrary threshold
            raise ValidationError("Transaction amount exceeds threshold.")

# Views
@require_http_methods(["GET", "POST"])
def transaction_view(request):
    """View to handle transaction creation and retrieval."""
    if request.method == "POST":
        try:
            customer_id = request.POST.get("customer_id")
            amount = request.POST.get("amount")
            customer = Customer.objects.get(id=customer_id)
            transaction = Transaction(customer=customer, amount=amount)
            transaction.clean()
            transaction.save()
            return JsonResponse({"message": "Transaction created successfully."}, status=201)
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer not found."}, status=404)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=400)
    else:  # GET
        transactions = Transaction.objects.all()
        transaction_data = [{