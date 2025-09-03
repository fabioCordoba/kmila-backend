from rest_framework.permissions import BasePermission


class IsSuperOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.rol == "administrator"
