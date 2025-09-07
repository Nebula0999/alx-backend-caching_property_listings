from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Allow access only to owners of an object or admin users.
    Assumes the object has an attribute `user` which is its owner.
    """
    def has_object_permission(self, request, view, obj):
        # Safe methods allowed to authenticated users if desired
        if request.method in permissions.SAFE_METHODS:
            return True
        # Admins always allowed
        if request.user and request.user.is_staff:
            return True
        # Otherwise user must own the object
        return getattr(obj, 'user', None) == request.user