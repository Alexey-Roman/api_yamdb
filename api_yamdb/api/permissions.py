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

class IsAdminOrReadOnly(permissions.BasePermission):
    """Проверка прав администратора."""
    message = 'Нужны права администратора.'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.role == 'admin'
                    or request.user.is_superuser)))


class IsAdminOrModeratirOrAuthor(permissions.BasePermission):
    """"Проверка прав для отзывов и комментариев."""
    message = 'Нужны права администратора/модератора или автора'

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.role == 'admin'
            or request.user.role == 'moderator'
            or request.user == obj.author
        )