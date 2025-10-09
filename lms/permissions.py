from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='moderators').exists():
            return True
        return False


class IsOwner(BasePermission):

    # def has_permission(self, request, view):
    #     return request.user == view.get_object().owner

    def has_object_permission(self, request, view, obj):
        print("----has_object_permission-----", obj.owner)
        return request.user == obj.owner



