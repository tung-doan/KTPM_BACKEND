from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserInfoView,
    UserRegistrationView,
    UserUpdateView,
    LoginView,
    CookieTokenRefreshView,
    LogoutAPIView,
    UserViewSet,
)

router = DefaultRouter()
router.register(r'', UserViewSet, basename='user')

urlpatterns = [
    path('info/', UserInfoView.as_view(), name='user-info'),
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('update/', UserUpdateView.as_view(), name='user-update'),
    path('login/', LoginView.as_view(), name='user-login'),
    path('token/refresh/', CookieTokenRefreshView.as_view(), name='token-refresh'),
    path('logout/', LogoutAPIView.as_view(), name='user-logout'),
    path('', include(router.urls)),
]