""" List of permissions for users """
# pylint:disable=E1101
# pylint:disable=broad-except
# pylint:disable=no-name-in-module
from rest_framework import permissions
from team.models import Team, Membership
from team_chat.models import TeamMessage
from private_chat.models import PrivateMessage


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


class IsTeamChatMessageOwner(permissions.BasePermission):
    """Grant permission to the owner of the message in a team chat"""

    # Override the method of BasePermission
    def has_permission(self, request, view):
        """Check permissions for the user of the request.
        The URL route holds the primary key of the message.

        Args:
            request (HTTP-Request object): GET, POST, PUT, DELETE requests
            view (APIView): Â View in team_chat app

        Returns:
            Boolean: True if the permission is granted. False if the permission
            is denied.
        """
        try:
            # Retrieve the message id from the parameters of the view
            message_id = view.kwargs.get("message_id", None)
            # Retrieve the message object
            message = TeamMessage.objects.get(id=message_id)
            if message.owner.id is not request.user.id:
                return False

        except Exception:
            # If an exception is encountered, it is only
            # because the request was anonymous, thus
            # deny access
            return False
        # Otherwise grant access
        return True


class IsTeamAccessAuthorized(permissions.BasePermission):
    """Permission used for checking authentication for users, who try to retrieve,
    post, update or delete a message in the team chatroom
    """

    def has_permission(self, request, view):
        """Check permissions for the user of the request.
        The URL route holds the primary key of the team.

        Args:
            request (HTTP-Request object): GET, POST, PUT, DELETE requests
            view (APIView): Â View in team_chat app

        Returns:
            Boolean: True if the permission is granted. False if the permission
            is denied.
        """

        try:
            # Retrieve the team id from the parameters of the view
            team_id = view.kwargs.get("team_id", None)
            # Access the requested team
            team = Team.objects.get(id=team_id)

            # See if the user is member of the requested team
            membership = Membership.objects.get_or_none(team=team, member=request.user)

            # See if the user is the owner of the team
            team_owner = team.owner == request.user

            # If the user is neither the owner of the team nor a member,
            # deny access
            if membership is None and not team_owner:
                return False
        except Exception:
            # If an exception is encountered, it is only
            # because the request was anonymous, thus
            # deny access
            return False
        # Otherwise grant access
        return True


class PrivateMessageListPermission(permissions.BasePermission):
    """Permission used for checking authentication for users, who try to retrieve,
    post, update or delete a message in the team chatroom
    """

    def has_permission(self, request, view):
        """Check permissions for the user of the request.
        The URL route holds the primary key of the team.

        Args:
            request (HTTP-Request object): GET, POST, PUT, DELETE requests
            view (APIView): Â View in team_chat app

        Returns:
            Boolean: True if the permission is granted. False if the permission
            is denied.
        """

        try:
            # Retrieve the team id from the parameters of the view
            team_id = request.GET.get("team_id", None)

            # Access the requested team
            team = Team.objects.get(id=team_id)

            # See if the user is member of the requested team
            membership = Membership.objects.get_or_none(team=team, member=request.user)

            # See if the user is the owner of the team
            team_owner = team.owner == request.user

            # If the user is neither the owner of the team nor a member,
            # deny access
            if membership is None and not team_owner:
                return False
        except Exception:
            # If an exception is encountered, it is only
            # because the request was anonymous, thus
            # deny access
            return False
        # Otherwise grant access
        return True


class PrivateMessageOwnerPermission(permissions.BasePermission):
    """Permission for owners of private messages"""

    def has_permission(self, request, view):
        message_id = view.kwargs.get("message_id", None)
        # If the user, who requested the access is the owner
        # of the message, then grant permission,
        # otherwise deny Access
        if message_id is not None:
            message = PrivateMessage.objects.get(id=message_id)
            if message.owner == request.user:
                return True
        return False
