from rest_framework.permissions import BasePermission



class DoctorPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user and not user.is_admin:
            return super().has_permission(request, view)
        return False
    
# # class AdminPermission(BasePermission):
    
    
