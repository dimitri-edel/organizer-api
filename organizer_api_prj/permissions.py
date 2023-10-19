""" List of permissions for users """
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """Grant manipulation only to the object owner"""

    # Override the method of BasePermission
    def has_object_permission(self, request, view, obj):
        # if the method is one of SAFE METHODS such as GET (READ)
        if request.method in permissions.SAFE_METHODS:
            # Permission granted
            return True
        # else if the user requesting is the owner of the object,
        # also grant access, otherwise do not!
        return obj.owner == request.user


class IsTeamMemberOrReadOnly(permissions.BasePermission):
    """Grant Permission only  to a of the team"""

    # Override the method of BasePermission
    def has_object_permission(self, request, view, obj):
        # if the method is one of SAFE METHODS such as GET (READ)
        if request.method in permissions.SAFE_METHODS:
            # Permission granted
            return True
        # else if the user requesting is member of the team
        # Membership.member
        # also grant access, otherwise do not!
        return obj.member == request.user


class IsOwnerOrTeamMemberOrReadOnly(permissions.BasePermission):
    """Grant permission to the task only to the owner of the task or a teammate"""

    # Override the method of BasePermission
    def has_object_permission(self, request, view, obj):
        # if the method is one of SAFE METHODS such as GET (READ)
        if request.method in permissions.SAFE_METHODS:
            # Permission granted
            return True
        # else if the user requesting is member of the team
        # Membership.member
        # also grant access, otherwise do not!
        return (obj.asigned_to == request.user) or (obj.owner == request.user)


class IsOwnerTeammateOrReadOnly(permissions.BasePermission):
    """Grant permission to the team only to owners and teammates"""

    # Override the method of BasePermission
    def has_object_permission(self, request, view, obj):
        # if the method is one of SAFE METHODS such as GET (READ)
        if request.method in permissions.SAFE_METHODS:
            # Permission granted
            return True
        # else if the user requesting is member of the team
        # Membership.member
        # also grant access, otherwise do not!
        return (obj.a == request.user) or (obj.owner == request.user)


class IsTeamPostAuthorized(permissions.BasePermission):
    """Permission used for checking authentication for users, who try to post
    in the team chatroom
    """

    def has_object_permission(self, request, view, obj):
        # if the method is one of SAFE METHODS such as GET (READ)
        if request.method in permissions.SAFE_METHODS:
            # Permission granted
            return True
        # else if the user requesting is member of the team
        # Membership.member
        # also grant access, otherwise do not!
        return (obj.team.membership.user == request.user) or (obj.owner == request.user)
