from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework.decorators import action
from django.utils.translation import gettext_lazy as _
from .models import User
from .serializers import CustomUserSerializer, UserRegistrationSerializer, LoginSerializer, LogoutSerializer, UserUpdateSerializer
from .permissions import UserPermission
from django.contrib.auth import update_session_auth_hash

class UserInfoView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object(), data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    serializer_class = LoginSerializer
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            access_token = serializer.validated_data['access']
            refresh_token = serializer.validated_data['refresh']
            response_data = {
                "user": CustomUserSerializer(user).data,
                "access": access_token,
                "refresh": refresh_token
            }
            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=access_token,
                max_age=60 * 60,
                httponly=True,
                secure=True,
                samesite='None',
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh_token,
                max_age=24 * 60 * 60,
                httponly=True,
                secure=True,
                samesite='None',
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CookieTokenRefreshView(TokenRefreshView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({"detail": "Không có refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            response = Response({"access": access_token}, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=access_token,
                max_age=60 * 60,
                httponly=True,
                secure=True,
                samesite='None',
            )
            return response
        except TokenError:
            return Response({"detail": "Refresh token không hợp lệ"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            response = Response({"message": "Đăng xuất thành công"}, status=status.HTTP_205_RESET_CONTENT)
            response.set_cookie(
                key='access_token',
                value='',
                path='/',
                secure=True,
                httponly=True,
                samesite='None',
            )
            response.set_cookie(
                key='refresh_token',
                value='',
                path='/',
                secure=True,
                httponly=True,
                samesite='None',
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [UserPermission]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager':
            return User.objects.filter(manager=user) | User.objects.filter(pk=user.pk)
        return User.objects.all()

    @action(detail=False, methods=['get'], url_path='unit/(?P<unit_code>[^/.]+)')
    def get_by_unit_code(self, request, unit_code=None):
        if request.user.role == 'manager' and request.user.unit_code and request.user.unit_code != unit_code:
            return Response({"detail": "Không có quyền truy cập mã đơn vị này"}, status=403)
        users = User.objects.filter(unit_code=unit_code, manager=request.user)
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='change-password')
    def change_password(self, request, pk=None):
        user = self.get_object()
        if request.user.role != 'manager':
            return Response({"detail": "Chỉ tổ trưởng được đổi mật khẩu"}, status=403)
        if user.manager != request.user and user != request.user:
            return Response({"detail": "Không có quyền đổi mật khẩu cho tài khoản này"}, status=403)
        unit_code = request.data.get('unit_code')
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({"detail": "Phải cung cấp mật khẩu mới"}, status=400)
        if unit_code and user.unit_code and unit_code != user.unit_code:
            return Response({"detail": "Mã đơn vị không khớp"}, status=400)
        user.set_password(new_password)
        user.save()
        if user == request.user:
            update_session_auth_hash(request, user)
        return Response({"detail": "Đổi mật khẩu thành công"})