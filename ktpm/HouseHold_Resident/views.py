from django.shortcuts import render
from .models import Citizen
from django.http import JsonResponse
from django.db.models import Q

def citizens(request):
    # Lấy các tham số lọc từ query string
    full_name = request.GET.get('full_name')
    household_id = request.GET.get('household_id')
    id_card_number = request.GET.get('id_card_number')
    birth_date = request.GET.get('birth_date')

    filters = Q()
    if full_name:
        filters &= Q(full_name__icontains=full_name)
    if household_id:
        filters &= Q(household_id=household_id)
    if id_card_number:
        filters &= Q(id_card_number__icontains=id_card_number)
    if birth_date:
        filters &= Q(birth_date=birth_date)

    mycitizens = list(Citizen.objects.filter(filters).values())
    return JsonResponse({
        "status": "success",
        "data": mycitizens
    })