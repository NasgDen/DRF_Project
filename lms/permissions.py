from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name="moderators").exists():
            return True
        return False


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner
