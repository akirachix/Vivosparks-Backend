from django.shortcuts import render

# Create your views here.
"""
This script defines views for handling API requests related to the `Market` and `InvestmentSimulation` models.
It includes functionality for creating, retrieving, updating, and soft-deleting both models using the `is_active` field
to manage soft deletes. The views use Django Rest Framework for handling GET, POST, PUT, and DELETE operations,
and logging is implemented for better traceability of the operations performed.
"""

import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializers import MarketSerializer, InvestmentSimulationSerializer
from market.models import Market
from investment_simulation.models import InvestmentSimulation
from django.shortcuts import get_object_or_404


logger = logging.getLogger(__name__)

"""
MarketListView:
    - Handles list operations for the `Market` model, including:
      - GET: Retrieves all active market entries.
      - POST: Creates a new market entry.
"""
class MarketListView(APIView):
   
    def get(self, request):
        logger.info("Fetching all active markets")
        markets = Market.objects.filter(is_active=True)
        serializer = MarketSerializer(markets, many=True)
        return Response(serializer.data)

  
    def post(self, request):
        logger.info("Creating a new market entry")
        serializer = MarketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Market entry created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Market creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
MarketDetailView:
    - Handles detailed operations on a single market entry, including:
      - GET: Retrieves a single market entry by its ID.
      - PUT: Updates an existing market entry.
      - DELETE: Soft deletes a market entry by marking it as inactive (using the `is_active` field).
"""
class MarketDetailView(APIView):

   
    def get(self, request, market_id):
        try:
            logger.info(f"Fetching market with ID: {market_id}")
            market = Market.objects.get(id=market_id, is_active=True)
            serializer = MarketSerializer(market)
            return Response(serializer.data)
        except Market.DoesNotExist:
            logger.error(f"Market with ID {market_id} not found or inactive")
            return Response(status=status.HTTP_404_NOT_FOUND)

 
    def put(self, request, market_id):
        try:
            logger.info(f"Updating market with ID: {market_id}")
            market = Market.objects.get(id=market_id, is_active=True)
            serializer = MarketSerializer(market, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Market with ID {market_id} updated successfully")
                return Response(serializer.data)
            logger.error(f"Market update failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Market.DoesNotExist:
            logger.error(f"Market with ID {market_id} not found or inactive")
            return Response(status=status.HTTP_404_NOT_FOUND)

  
    def delete(self, request, market_id):
        try:
            logger.info(f"Attempting to deactivate (soft delete) market with ID: {market_id}")
            market = Market.objects.get(id=market_id, is_active=True)
            market.is_active = False
            market.save()
            logger.info(f"Market with ID {market_id} deactivated successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Market.DoesNotExist:
            logger.error(f"Market with ID {market_id} not found or already deactivated")
            return Response(status=status.HTTP_404_NOT_FOUND)

"""
InvestmentSimulationListView:
    - Handles list operations for the `InvestmentSimulation` model, including:
      - GET: Retrieves all investment simulations.
      - POST: Creates a new investment simulation entry.
"""
class InvestmentSimulationListView(APIView):
 
    def get(self, request):
        logger.info("Fetching all investment simulations")
        simulations = InvestmentSimulation.objects.all()
        serializer = InvestmentSimulationSerializer(simulations, many=True)
        return Response(serializer.data)

    def post(self, request):
        logger.info("Creating a new investment simulation")
        serializer = InvestmentSimulationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info("Investment simulation created successfully")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Investment simulation creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

"""
InvestmentSimulationDetailView:
    - Handles detailed operations on a single investment simulation entry, including:
      - GET: Retrieves a single investment simulation by its ID.
      - PUT: Updates an existing investment simulation entry.
      - DELETE: Soft deletes an investment simulation entry (implementation for actual soft delete needed).
"""
class InvestmentSimulationDetailView(APIView):

    def get(self, request, simulation_id):
        try:
            logger.info(f"Fetching investment simulation with ID: {simulation_id}")
            simulation = InvestmentSimulation.objects.get(id=simulation_id)
            serializer = InvestmentSimulationSerializer(simulation)
            return Response(serializer.data)
        except InvestmentSimulation.DoesNotExist:
            logger.error(f"Investment simulation with ID {simulation_id} not found")
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, simulation_id):
        try:
            logger.info(f"Updating investment simulation with ID: {simulation_id}")
            simulation = InvestmentSimulation.objects.get(id=simulation_id)
            serializer = InvestmentSimulationSerializer(simulation, data=request.data)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Investment simulation with ID {simulation_id} updated successfully")
                return Response(serializer.data)
            logger.error(f"Investment simulation update failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except InvestmentSimulation.DoesNotExist:
            logger.error(f"Investment simulation with ID {simulation_id} not found")
            return Response(status=status.HTTP_404_NOT_FOUND)

    
    def delete(self, request, simulation_id):
        try:
            logger.info(f"Attempting to soft delete investment simulation with ID: {simulation_id}")
            simulation = InvestmentSimulation.objects.get(id=simulation_id)
            simulation.is_active = True
            simulation.save()
            logger.info(f"Investment simulation with ID {simulation_id} soft deleted successfully")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except InvestmentSimulation.DoesNotExist:
            logger.error(f"Investment simulation with ID {simulation_id} not found")
            return Response(status=status.HTTP_404_NOT_FOUND)


