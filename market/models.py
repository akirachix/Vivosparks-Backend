from django.db import models

# Create your models here.
from django.db import models



"""
The Market model represents investment markets, including the market's 
name, risk level, and description. It helps categorize various markets, 
providing insight into their trend risks and nature for investors.
"""
class Market(models.Model):
    market_id = models.AutoField(primary_key=True)
    market_name = models.CharField(max_length=100)
    risk_level = models.CharField(max_length=20)
    description = models.TextField()
    
    is_active = models.BooleanField(default=True)
    def soft_delete(self):
        self.is_active = False
        self.save()
    
    def __str__(self):
        return self.market_name