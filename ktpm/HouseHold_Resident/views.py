from django.db.models import Count
from .models import Citizen, Household
from django.http import JsonResponse
from django.db.models import Q
from datetime import date
from django.views.decorators.csrf import csrf_exempt
import json
from django.views.decorators.http import require_http_methods


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
    
def statistics(request):
    # Lấy các tham số lọc từ query string
    criteria = request.GET.get('criteria')  # 'gender', 'job', 'age'
    result = {}
    
    if criteria == 'gender':
        # Thống kê theo giới tính
        data = Citizen.objects.values('gender').annotate(count=Count('citizen_id'))
        result = {item['gender']: item['count'] for item in data}
    elif criteria == 'job':
        # Thống kê theo nghề nghiệp
        data = Citizen.objects.values('job').annotate(count=Count('citizen_id'))
        result = {item['job']: item['count'] for item in data}
    elif criteria == 'age':
        today = date.today()
        age_groups = {'<18': 0, '18-30': 0, '31-50': 0, '>50': 0}
        for c in Citizen.objects.all():
            if c.birth_date:
                age = today.year - c.birth_date.year - ((today.month, today.day) < (c.birth_date.month, c.birth_date.day))
                if age < 18:
                    age_groups['<18'] += 1
                elif age <= 30:
                    age_groups['18-30'] += 1
                elif age <= 50:
                    age_groups['31-50'] += 1
                else:
                    age_groups['>50'] += 1
        result = age_groups
    else:
        return JsonResponse({
            "status": "error",
            "message": "Invalid criteria"
        })
    
    return JsonResponse({
        "status": "success",
        "criteria": criteria,
        "data": result
    })
    
@csrf_exempt
@require_http_methods(["POST"])
def add_citizen(request):
    try:
        data = json.loads(request.body)
        household_id = data.get('household_id')
        household = Household.objects.get(pk=household_id)
        citizen = Citizen.objects.create(
            household=household,
            full_name=data.get('full_name'),
            gender=data.get('gender'),
            birth_date=data.get('birth_date'),
            birth_place=data.get('birth_place'),
            origin_place=data.get('origin_place'),
            job=data.get('job'),
            workplace=data.get('workplace'),
            id_card_number=data.get('id_card_number'),
            id_card_issue_date=data.get('id_card_issue_date'),
            id_card_issue_place=data.get('id_card_issue_place'),
            previous_residence=data.get('previous_residence')
        )
        return JsonResponse({"status": "success", "citizen_id": citizen.citizen_id})
    except Household.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Household not found"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)  
    
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_citizen(request,id_card_number ):
    try:
        citizen = Citizen.objects.get(id_card_number=id_card_number)
        citizen.delete()
        return JsonResponse({"status": "success"})
    except Citizen.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Citizen not found"}, status=400)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)