from rest_framework import permissions
from group.models import GroupMember


class UserPermission(permissions.BasePermission):
    message = 'User not allowed.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        queryset = GroupMember.objects.filter(group=obj)
        for object in queryset:
            if user == object.user:
                return True
        return False


class CreatorPermission(permissions.BasePermission):
    message = 'User not allowed.'

    def has_object_permission(self, request, view, obj):
        user = request.user
        if user == object.creator:
            return True
        return False
