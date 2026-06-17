from rest_framework.permissions import BasePermission 



class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.role.is_authenticated and 
            request.user.role == 'admin'
        )