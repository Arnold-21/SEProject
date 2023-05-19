from rest_framework.permissions import BasePermission

class isUserObjectPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.id
    
class usersDestinationPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.userID
    
class isAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == "Admin" 