from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user

class IsAuthor(permissions.BasePermission):
    message = "You are not an author"

    def has_permission(self, request, view):
        user_groups = request.user.groups.values_list("name", flat=True)
        if "author" in user_groups:
            return True
        return False