from rest_framework import serializers
from .models import Citizen, Household

class CitizenSerializer(serializers.ModelSerializer):
    household = serializers.PrimaryKeyRelatedField(
        queryset=Household.objects.all(), required=False, allow_null=True
    )
    class Meta:
        model = Citizen
        fields = '__all__'

class HouseholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Household
        fields = '__all__'