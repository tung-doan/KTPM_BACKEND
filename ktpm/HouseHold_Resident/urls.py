from django.urls import path
from . import views

urlpatterns = [
    path('citizens/', views.citizens, name='citizens'),
]