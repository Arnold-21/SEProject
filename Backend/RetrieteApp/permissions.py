from rest_framework.permissions import BasePermission
from .models import User

#Checking if the user has permission to see the user detail
class isUserObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id
    
#Check if the user has permission to modify a destination object, basically if the destination is his
class usersDestinationPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return User.objects.get(email=obj.userID).id == request.user.id
    
# Check if the user has admin privileges
class isAdminRole(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Admin" 