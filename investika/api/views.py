from django.shortcuts import render

# Create your views here.
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from virtual_money.models import VirtualMoney
from .serializers import VirtualMoneySerializer


# Set up logging
logger = logging.getLogger(__name__)


class VirtualMoneyView(APIView):
    """
    Handles creating and listing VirtualMoney instances.
    """

    def post(self, request):
        """
        Create a new VirtualMoney instance.
        """
        logger.info('POST request received for VirtualMoney')
        serializer = VirtualMoneySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info('VirtualMoney created successfully')
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error('Validation errors: %s', serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    """
    List all VirtualMoney instances.
    """
    def get(self, request):
        """
        Retrieve a list of all VirtualMoney instances.
        """
        logger.info('GET request received for VirtualMoney list')
        virtual_moneys = VirtualMoney.objects.all()
        serializer = VirtualMoneySerializer(virtual_moneys, many=True)
        return Response(serializer.data)

class VirtualMoneyDetailView(APIView):
    def get(self, request, id):
        try:
            virtual_money = VirtualMoney.objects.get(id=id)
            serializer = VirtualMoneySerializer(virtual_money)
            return Response(serializer.data)
        except VirtualMoney.DoesNotExist:
            return Response({"error": "Virtual Money not found"}, status=status.HTTP_404_NOT_FOUND)
    

    def patch(self, request, virtual_money_id):
        try:
            virtual_money = VirtualMoney.objects.get(virtual_money_id=virtual_money_id)
            serializer = VirtualMoneySerializer(virtual_money, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except VirtualMoney.DoesNotExist:
            return Response({"error": "VirtualMoney not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, virtual_money_id):
        try:
            virtual_money = VirtualMoney.objects.get(virtual_money_id=virtual_money_id)
            virtual_money.is_active = False
            virtual_money.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except VirtualMoney.DoesNotExist:
            return Response({"error": "VirtualMoney not found"}, status=status.HTTP_404_NOT_FOUND)