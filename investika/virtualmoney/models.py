from django.db import models

class VirtualMoney(models.Model):
    """
    Define the VirtualMoney model with:
    Auto-incrementing primary key
    Amount field (max 10 digits, 2 decimals)
    Creation timestamp
    String representation
    """
    id = models.AutoField(primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    date_granted = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"Virtual Money - {self.amount}"
