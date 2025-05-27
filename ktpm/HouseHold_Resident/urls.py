from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CitizenViewSet, HouseholdViewSet

router = DefaultRouter()
router.register(r'citizens', CitizenViewSet, basename='citizen')
router.register(r'households', HouseholdViewSet, basename='household')
urlpatterns = router.urls