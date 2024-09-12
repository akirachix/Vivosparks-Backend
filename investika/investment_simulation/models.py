from django.db import models
from market.models import Market
"""
 The InvestmentSimulation model records details of simulated investments made by users.
 It stores information such as the market in which the investment is made, the amount invested,
 the outcome (profit or loss), and other metadata like investment date and associated market data.
 This model also includes a method for soft deletion, which marks an entry as inactive without permanently removing it.
"""
class InvestmentSimulation(models.Model):
    id = models.AutoField(primary_key=True, serialize=False)
    market_id = models.ForeignKey(Market, on_delete=models.CASCADE)
    amount_invested = models.DecimalField(decimal_places=2, max_digits=10)
    investment_date = models.DateTimeField(auto_now_add=True)
    outcome = models.CharField(max_length=10)
    profit_loss = models.DecimalField(decimal_places=2, max_digits=10)
    is_active = models.BooleanField(default=True)

    def soft_delete(self):
        self.is_active = False
        self.save()
    def __str__(self):
        return str(self.simulation_id)