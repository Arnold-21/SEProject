from rest_framework.permissions import BasePermission
from .models import User

class isUserObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id
    
class usersDestinationPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return User.objects.get(email=obj.userID).id == request.user.id
    
class isAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Admin" 