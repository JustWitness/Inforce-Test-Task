from rest_framework import permissions

from users.enums import UserRole


class IsRestaurant(permissions.BasePermission):
    message = "You must be a restaurant to perform this action"

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == UserRole.RESTAURANT)

class IsEmployee(permissions.BasePermission):
    message = "You must be a employee to perform this action"

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == UserRole.EMPLOYEE)

class IsAdmin(permissions.BasePermission):
    message = "You must be a admin to perform this action"

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.role == UserRole.ADMIN)
