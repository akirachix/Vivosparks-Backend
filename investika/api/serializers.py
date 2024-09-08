from rest_framework import serializers
from market.models import Market 
from investment_simulation.models import InvestmentSimulation

        
"""      
Serializer for the Market model which include all fields in the serialized output  
"""
       
class MarketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Market
        fields = '__all__'
        
"""        
Serializer for the InvestmentSimulation model which include all fields in the serialized output
"""
class InvestmentSimulationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentSimulation
        fields = '__all__'


