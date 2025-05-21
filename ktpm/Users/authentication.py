import logging
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed

# Thiết lập logger
logger = logging.getLogger(__name__)

class CookieJWTAuthentication(JWTAuthentication):
    """
    Custom JWT authentication class that retrieves the JWT token from the 'access_token' cookie
    instead of the Authorization header.
    """
    def authenticate(self, request):
        # Lấy token từ cookie
        token = request.COOKIES.get('access_token')
        
        # Kiểm tra token có tồn tại và không rỗng
        if not token or token.strip() == '':
            logger.debug("No access token found in cookies")
            return None

        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"Token from cookies: {token}")

        try:
            # Xác thực token
            validated_token = self.get_validated_token(token)
            # Lấy user từ token
            user = self.get_user(validated_token)
            return user, validated_token
        except InvalidToken:
            raise AuthenticationFailed("Token không hợp lệ hoặc đã hết hạn")
        except TokenError as e:
            raise AuthenticationFailed(f"Lỗi token: {str(e)}")
        except AuthenticationFailed as e:
            raise AuthenticationFailed(f"Không tìm thấy người dùng: {str(e)}")