from rest_framework import permissions

class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.role in ['manager', 'deputy', 'accountant']
        if request.method in ['POST', 'PUT', 'PATCH']:
            return request.user.is_authenticated and request.user.role == 'manager'
        if request.method == 'DELETE':
            return request.user.is_authenticated and request.user.role == 'manager'
        return False