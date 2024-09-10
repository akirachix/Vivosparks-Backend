from django.db import models
from django.contrib.auth.models import User
from django.conf import settings



class Assessment(models.Model):
    """
    Unique identifier for each assessment (Primary Key)
    Reference to the user who took the assessment (Foreign Key)
    Amount spent on non-essential items
    Amount spent on essential items
    Amount saved
    Amount invested
    Timestamp for when the assessment was taken
    Indicator for whether the assessment is active (Soft delete support)
    """

    assessment_id = models.IntegerField(primary_key=True)
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True,default=None)
    spending_on_wants = models.DecimalField(max_digits=10, decimal_places=2)
    spending_on_needs = models.DecimalField(max_digits=10, decimal_places=2)
    savings = models.DecimalField(max_digits=10, decimal_places=2)
    investment = models.DecimalField(max_digits=10, decimal_places=2)
    taken_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Assessment {self.assessment_id} by User {self.user_id}"
    

