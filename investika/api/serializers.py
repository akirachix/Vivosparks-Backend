from rest_framework import serializers
from virtual_money.models import VirtualMoney


class VirtualMoneySerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualMoney
        fields = '__all__'