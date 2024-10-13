from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    #내가 만든 obj에 대해서만 접근 허용
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsVoter(permissions.BasePermission):
    #내가 만든 Voter에 대해서만 전부 허용
    def has_object_permission(self, request, view, obj):
        return obj.voter == request.user