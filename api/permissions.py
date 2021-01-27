from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSellerOrReadOnly(BasePermission):
    """
    O usuário é um Vendedor, ou somente leitura
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_authenticated and
            request.user.is_seller
        )


class IsSellerOrClient(BasePermission):
    """
    O usuário precisa estar autenticado como vendedor ou cliente, sendo que cliente só poderá usar GET, HEAD e OPTIONS
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            (request.user.is_seller or (request.user.is_client and request.method in SAFE_METHODS))
        )


class IsSeller(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.is_seller
        )
