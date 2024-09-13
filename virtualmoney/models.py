from django.db import models
from django.conf import settings

class VirtualMoney(models.Model):
    """
    Define the VirtualMoney model with:
    Auto-incrementing primary key
    Amount field (max 10 digits, 2 decimals)
    Creation timestamp
    String representation
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, default=None)  # Correct field name
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_granted = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Add an active flag for soft deletion
    
    def soft_delete(self):
        self.is_active = False
        self.save()
  
    def __str__(self):
        return f"Virtual Money - {self.amount}"
