from django.db.models import Count
from .models import Citizen, Household
from django.http import JsonResponse
from django.db.models import Q
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CitizenSerializer,HouseholdSerializer
from rest_framework import viewsets


class CitizenViewSet(viewsets.ModelViewSet):
    queryset = Citizen.objects.all()
    serializer_class = CitizenSerializer
    
    def get_queryset(self):
        return Citizen.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            data = super().create(request, *args, **kwargs)
            
            return Response(
                {"message": "Citizen created successfully",
                 "data":data.data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            response.data['message'] = "Citizen updated successfully"
            return response
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, *args, **kwargs):
        try:
            data = super().destroy(request, *args, **kwargs)
            return Response(
                {"message": "Citizen deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
class HouseholdViewSet(viewsets.ModelViewSet):
    queryset = Household.objects.all()
    serializer_class = HouseholdSerializer
    
    def get_queryset(self):
        return Household.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            data = super().create(request, *args, **kwargs)
            return Response(
                {"message": "Household created successfully",
                 "data":data.data},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            response.data['message'] = "Household updated successfully"
            return response
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def destroy(self, request, *args, **kwargs):
        try:
            super().destroy(request, *args, **kwargs)
            return Response(
                {"message": "Household deleted successfully"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )