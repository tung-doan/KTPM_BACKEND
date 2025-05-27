from rest_framework import permissions

class HouseHold_ResidentPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return request.user.role in ['manager', 'deputy', 'accountant']
        if request.method in ['POST', 'PUT', 'DELETE', 'PATCH']:
            return request.user.role == 'manager'
        return False