from rest_framework import serializers
from .models import BudgetData

class BudgetDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = BudgetData
        fields = '__all__'
