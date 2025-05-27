from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .models import User

class CustomUserSerializer(serializers.ModelSerializer):
    manager = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='manager'), allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'unit_code', 'manager']
        read_only_fields = ['id', 'manager']

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    unit_code = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'unit_code', 'password']

    def validate(self, data):
        role = data.get('role')
        unit_code = data.get('unit_code')

        # Kiểm tra unit_code và tự động đặt manager
        if role == 'manager':
            if unit_code and User.objects.filter(unit_code=unit_code, role='manager').exists():
                raise serializers.ValidationError("Mã tổ trưởng (unit_code) đã tồn tại")
        else:  # deputy hoặc accountant
            if not unit_code:
                raise serializers.ValidationError("Phải cung cấp mã tổ trưởng (unit_code)")
            try:
                manager_user = User.objects.get(unit_code=unit_code, role='manager')
                data['manager'] = manager_user
            except User.DoesNotExist:
                raise serializers.ValidationError("Mã tổ trưởng (unit_code) không hợp lệ")

        # Kiểm tra email và username
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email đã tồn tại")
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Tên đăng nhập đã tồn tại")

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data['role'],
            unit_code=validated_data.get('unit_code'),
            manager=validated_data.get('manager')
        )
        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            if not user:
                raise serializers.ValidationError(
                    "Không thể đăng nhập với thông tin cung cấp",
                    code='authentication'
                )
        else:
            raise serializers.ValidationError(
                "Phải cung cấp tên đăng nhập và mật khẩu",
                code='authentication'
            )

        refresh = RefreshToken.for_user(user)
        attrs['user'] = user
        attrs['refresh'] = str(refresh)
        attrs['access'] = str(refresh.access_token)
        return attrs

class LogoutSerializer(serializers.Serializer):
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if refresh_token is None:
            return Response(
                {"detail": "Không tìm thấy refresh_token trong cookie"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {"detail": "Token không hợp lệ hoặc đã hết hạn"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Optional: Xóa cookie khỏi trình duyệt
        response = Response({"detail": "Đăng xuất thành công"}, status=status.HTTP_205_RESET_CONTENT)
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')  # nếu bạn có access_token trong cookie

        return response

class UserUpdateSerializer(serializers.ModelSerializer):
    manager = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(role='manager'), 
        required=False, 
        allow_null=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'unit_code', 'manager']
        extra_kwargs = {
            'username': {'required': False},
            'email': {'required': True},
            'role': {'required': False},
            'unit_code': {'required': False},
        }

    def validate_email(self, value):
        if User.objects.exclude(pk=self.instance.pk).filter(email=value).exists():
            raise serializers.ValidationError("Email đã tồn tại")
        return value

    def validate_role(self, value):
        user = self.context['request'].user
        if user.role != 'manager' and value != self.instance.role:
            raise serializers.ValidationError("Chỉ tổ trưởng được thay đổi vai trò")
        return value

    def validate_unit_code(self, value):
        user = self.context['request'].user
        if value and user.role == 'manager' and user.unit_code and value != user.unit_code:
            raise serializers.ValidationError("Tổ trưởng chỉ được sử dụng mã đơn vị của mình")
        return value

    def validate_manager(self, value):
        user = self.context['request'].user
        role = self.instance.role if self.instance else self.initial_data.get('role')
        if role in ['deputy', 'accountant'] and not value:
            raise serializers.ValidationError("Tổ phó và kế toán phải có người quản lý")
        if role == 'manager' and value is not None:
            raise serializers.ValidationError("Tổ trưởng không được có người quản lý")
        if value and user.role == 'manager' and value != user:
            raise serializers.ValidationError("Tổ trưởng chỉ được đặt mình là người quản lý")
        return value

    def validate_username(self, value):
        if User.objects.exclude(pk=self.instance.pk).filter(username=value).exists():
            raise serializers.ValidationError("Tên đăng nhập đã tồn tại")
        return value