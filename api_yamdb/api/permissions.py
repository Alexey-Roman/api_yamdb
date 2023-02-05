from rest_framework import permissions

from users.enums import UserRole


class AdministratorEdit(permissions.BasePermission):
    """Проверка на раоль администратора либо суперпользователя"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.role == UserRole.admin.name
            or request.user.is_superuser
        )


class IsAnonymous(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return not request.user.is_authenticated
