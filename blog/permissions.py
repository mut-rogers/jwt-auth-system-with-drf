from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Object level permission to only allow post authors to delete them.
    The model instance has the 'author' attribute
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            # Only Read permissions for GET, HEAD, and OPTIONS
            return True

        # Edit permissions for authors
        return obj.author == request.user
