from django.urls import path
from . import views

urlpatterns = [
    path('api/citizens/', views.citizens, name='citizens'),
    path('api/statistics/', views.statistics, name='statistics'),
]