# projects/permissions.py
from rest_framework import permissions

class IsTrainerOrAssignedTraineeOrReadOnly(permissions.BasePermission):
    """
    Trainer can create/edit/delete any project.
    Assigned trainee can update the project (but only certain fields ideally).
    ReadOnly for others.
    """
    def has_permission(self, request, view):
        # Allow read-only access for all
        if request.method in permissions.SAFE_METHODS:
            return True
        # For write operations check auth
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read-only for all
        if request.method in permissions.SAFE_METHODS:
            return True

        # If user is trainer => allow (check profile)
        if hasattr(request.user, 'profile') and request.user.profile.is_trainer:
            return True

        # If user is the assigned trainee, allow update (but not delete)
        if obj.assigned_to == request.user:
            # allow PUT/PATCH but not DELETE
            if request.method in ('PUT', 'PATCH'):
                return True
            # disallow delete by trainee
            if request.method == 'DELETE':
                return False

        return False
