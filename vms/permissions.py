from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAdminUser


class IsAdminOrAuthendicatedReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        return bool(request.user and request.user.is_authenticated and request.user.is_staff)


class IsVendor(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.account_type == "V")


class IsPurchaser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.account_type == "P")


class IsAdminOrPurchaser(BasePermission):
    def has_permission(self, request, view):
        return IsAdminUser().has_permission(request, view) or IsPurchaser().has_permission(request, view)


class IsAdminOrVendor(BasePermission):
    def has_permission(self, request, view):
        return IsAdminUser().has_permission(request, view) or IsVendor().has_permission(request, view)
