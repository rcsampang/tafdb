from rest_framework import permissions

class IsAdminUser(permissions.BasePermission):
    """
    Custom permission to only allow users with 'admin' user_type.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.profile.user_type == 'admin'

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Read-only for authenticated users, R/W for admin users.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False # Must be authenticated

        if request.method in permissions.SAFE_METHODS: # GET, HEAD, OPTIONS
            return True # Authenticated users can read

        # Write permissions are only allowed to admin users.
        return request.user.profile.user_type == 'admin'

class CanDownloadAttachment(permissions.BasePermission):
    """
    Allow any authenticated user to download attachments.
    Specific logic for who can download what might be handled in the view if needed.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
