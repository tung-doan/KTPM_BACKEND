from .models import Citizen, Household
from rest_framework.response import Response
from rest_framework import status
from .serializers import CitizenSerializer,HouseholdSerializer
from rest_framework import viewsets
from .permissions import HouseHold_ResidentPermission


class CitizenViewSet(viewsets.ModelViewSet):
    queryset = Citizen.objects.all()
    serializer_class = CitizenSerializer
    permission_classes = [HouseHold_ResidentPermission]
    def get_queryset(self):
        return Citizen.objects.all()
    
    def create(self, request, *args, **kwargs):
        try:
            data = super().create(request, *args, **kwargs)
            household_id = request.data.get('household')
            if household_id:
                household = Household.objects.get(pk=household_id)
                household.number_people += 1
                household.save()
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
    permission_classes = [HouseHold_ResidentPermission]

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