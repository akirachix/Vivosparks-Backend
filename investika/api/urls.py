
"""
urls.py:
    This file defines the URL routing for the API endpoints related to the `Market` and `InvestmentSimulation` models.
    It maps specific URL patterns to the appropriate views, enabling the API to handle requests for each resource.
"""

from django.urls import path
from .views import MarketListView, MarketDetailView, InvestmentSimulationListView, InvestmentSimulationDetailView

urlpatterns = [
    path('markets/', MarketListView.as_view(), name='market-list'),
    path('markets/<int:market_id>/', MarketDetailView.as_view(), name='market-detail'),
    path('investment-simulations/', InvestmentSimulationListView.as_view(), name='investment-simulation-list'),
    path('investment-simulations/<int:simulation_id>/', InvestmentSimulationDetailView.as_view(), name='investment-simulation-detail'),
]

