from rest_framework import permissions


class IsAdminOrAuthendicatedReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.account_type == "V")


class IsPurchaser(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.account_type == "P")


class IsAdminOrPurchaser(permissions.BasePermission):
    def has_permission(self, request, view):
        return permissions.IsAdminUser().has_permission(request, view) or IsPurchaser().has_permission(request, view)


class IsAdminOrVendor(permissions.BasePermission):
    def has_permission(self, request, view):
        return permissions.IsAdminUser().has_permission(request, view) or IsVendor().has_permission(request, view)
