from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CitizenViewSet

router = DefaultRouter()
router.register(r'citizens', CitizenViewSet, basename='citizen')

urlpatterns = router.urls