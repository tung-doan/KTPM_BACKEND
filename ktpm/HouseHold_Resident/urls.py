from django.urls import path
from . import views

urlpatterns = [
    path('api/citizens/', views.citizens, name='citizens'),
    path('api/statistics/', views.statistics, name='statistics'),
    path('api/citizen/add/', views.add_citizen, name='add_citizen'),
    path('api/citizen/delete/', views.delete_citizen, name='delete_citizen'),
]