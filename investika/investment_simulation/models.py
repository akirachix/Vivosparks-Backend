from django.db import models
from market.models import Market

class InvestmentSimulation(models.Model):
    simulation_id = models.AutoField(primary_key=True, serialize=False)
    market_id = models.ForeignKey(Market, on_delete=models.CASCADE)
    amount_invested = models.DecimalField(decimal_places=2, max_digits=10)
    investment_date = models.DateTimeField(auto_now_add=True)
    outcome = models.CharField(max_length=10)
    profit_loss = models.DecimalField(decimal_places=2, max_digits=10) 

    def soft_delete(self):
        self.is_active = False
        self.save()

    def __str__(self):
        return str(self.simulation_id)

