from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        print("Объект", obj)
        print("User", request.user)
        return request.user == obj
