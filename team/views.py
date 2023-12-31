""" Views for team app """
from rest_framework.views import APIView
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from organizer_api_prj.permissions import (
    IsOwnerOrReadOnly,
    IsTeamMemberOrReadOnly,
    IsTeamAccessAuthorized,
)
from .models import Team, Membership
from .serializers import TeamSerializer, TeamMembershipSerializer

# pylint: disable=E1101
# pylint: disable=unused-argument


class TeamList(generics.ListCreateAPIView):
    """TeamList provides a view for listing teams and a post method for creating teams"""

    # TeamList allows user to view teams, or create their own teams
    # Allow creating teams only to authenticated users
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    # fields for SearchFilter
    search_fields = [
        "owner__username",
        "name",
    ]
    # fields for OrderingFilter
    ordering_fields = [
        "owner__username",
    ]
    # fields for DjangoFilterBackend
    filterset_fields = [
        "owner__username",
        "name",
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TeamDetails(generics.RetrieveUpdateDestroyAPIView):
    """TeamDetails provides views for updating, deleting and retrieving
    individual teams
    """

    # TeamDetails allows the user to delete or update their own teams
    serializer_class = TeamSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Team.objects.all()


class TeamMembershipList(generics.ListCreateAPIView):
    """TeamMembershipList provides a view for listing Memberships
    and creating new memberships
    """

    # TeamMembershipList allows the user to join teams
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamMembershipSerializer

    def get_queryset(self):
        # query set where the user is not the owner of the team
        exclude_user_set = Membership.objects.exclude(team__owner=self.request.user)
        # A set where the user is the member of the team
        filtered_set = exclude_user_set.filter(member=self.request.user)

        return filtered_set

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)


class TeamMembershipDetails(generics.RetrieveAPIView):
    """TeamMembershipDetails allows users to leave teams"""

    serializer_class = TeamMembershipSerializer
    permission_classes = [IsTeamMemberOrReadOnly]

    def get_queryset(self):
        return Membership.objects.all()


class LeaveTeam(APIView):
    """
    LeaveTeam allows the user to quit(delete) a team membership by providing
    the team_id in the request
    """

    # Attribute of APIView that creates a form for the object
    serializer_class = TeamSerializer
    # Attribute of APIView that allows to manage permissions
    permission_classes = [IsTeamMemberOrReadOnly]

    def get_object(self, team_id):
        """retrieve the object from the database"""
        try:
            team = Team.objects.get(id=team_id)
            membership = Membership.objects.get(member=self.request.user, team=team)

            # Call an method of APIView to check the permissions
            # If the user does not have permission, the method will
            # throw the 403 Error (Forbidden)
            self.check_object_permissions(self.request, membership)
            return membership
        except Membership.DoesNotExist as exc:
            raise Http404 from exc

    def delete(self, request, team_id):
        """delete object from database"""
        memebership = self.get_object(team_id)
        memebership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeamMates(generics.ListAPIView):
    """List of all members of all teams owned by the current user"""

    serializer_class = TeamMembershipSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Membership.objects.filter(team__owner=self.request.user)


class TeamMembers(APIView):
    """List of all members for a particular team"""

    # The class that holds permissions to the team chat for users
    permission_classes = [IsTeamAccessAuthorized]

    def get(self, request, team_id):
        """Process the GET request

        Args:
            request (GET-Request): The GET request sent by the client
            team_id (Integer): The PK of the requested team

        Returns:
            Serialized JSON: List of team member of the respective team
        """
        team = Team.objects.get(id=team_id)

        memberships = Membership.objects.filter(team=team)
        data = []
        # append the team owner
        owner = {}
        owner["user_id"] = team.owner.id
        owner["username"] = team.owner.username
        data.append(owner)
        # append all team members
        for member in memberships:
            user = {}
            user["user_id"] = member.member.id
            user["username"] = member.member.username
            data.append(user)

        # Return a dictionary with the number of messages found
        return Response(data, status=status.HTTP_200_OK)


class TeamMembersCount(APIView):
    """Return number of members in a specific team"""

    # The class that holds permissions to the team chat for users
    permission_classes = [IsTeamAccessAuthorized]

    def get(self, request, team_id):
        """Process the GET request

        Args:
            request (GET-Request): The GET request sent by the client
            team_id (Integer): The PK of the requested team

        Returns:
            Serialized JSON: List of team member of the respective team
        """
        team = Team.objects.get(id=team_id)
        memberships = Membership.objects.filter(team=team)
        count = memberships.count()
        # Return a dictionary with the number of messages found
        return Response({"count": count}, status=status.HTTP_200_OK)
