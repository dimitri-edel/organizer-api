""" Views for team app """
from rest_framework.views import APIView
from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from django.http import Http404
from organizer_api_prj.permissions import IsOwnerOrReadOnly, IsTeamMemberOrReadOnly
from .models import Team, Membership
from .serializers import TeamSerializer, TeamMembershipSerializer

# pylint: disable=E1101
# pylint: disable=unused-argument

class TeamList(generics.ListCreateAPIView):
    """ TeamList provides a view for listing teams and a post method for creating teams"""
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
        'owner__username',
        'name',
    ]
    # fields for OrderingFilter
    ordering_fields = [
        'owner__username',
    ]
    # fields for DjangoFilterBackend
    filterset_fields = [
        'owner__username',
        'name',
    ]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TeamDetails(generics.RetrieveUpdateDestroyAPIView):
    """ TeamDetails provides views for updating, deleting and retrieving 
        individual teams
    """
    # TeamDetails allows the user to delete or update their own teams
    serializer_class = TeamSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Team.objects.all()


class TeamMembershipList(generics.ListCreateAPIView):
    """ TeamMembershipList provides a view for listing Memberships
        and creating new memberships
    """
    # TeamMembershipList allows the user to join teams
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamMembershipSerializer

    def get_queryset(self):
        return Membership.objects.exclude(team__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)


class TeamMembershipDetails(generics.RetrieveDestroyAPIView):
    """TeamMembershipDetails allows users to leave teams"""
    serializer_class = TeamMembershipSerializer
    permission_classes = [IsTeamMemberOrReadOnly]

    def get_queryset(self):
        return Membership.objects.all()


class LeaveTeam(APIView):
    """LeaveTeam allows the user to quit a team membership by providing the team_id in the request"""

    # Attribute of APIView that creates a form for the object
    serializer_class = TeamSerializer
    # Attribute of APIView that allows to manage permissions
    permission_classes = [IsTeamMemberOrReadOnly]

    def get_object(self, team_id):
        """retrieve the object from the database"""
        try:
            team = Team.objects.get(id=team_id)
            membership = Membership.objects.get(
                member=self.request.user, team=team)

            # Call an method of APIView to check the permissions
            # If the user does not have permission, the method will
            # thrwo the 403 Error (Forbidden)
            self.check_object_permissions(self.request, membership)
            return membership
        except Membership.DoesNotExist as exc:
            raise Http404 from exc

    def delete(self, request, team_id):
        """ delete object from database """
        memebership = self.get_object(team_id)
        memebership.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeamMates(generics.ListAPIView):    
    """List of all members of all teams owned by the current user"""
    serializer_class = TeamMembershipSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Membership.objects.filter(team__owner=self.request.user)
