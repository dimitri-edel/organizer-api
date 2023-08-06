from rest_framework import generics, permissions, filters
from organizer_api_prj.permissions import IsOwnerOrReadOnly, IsTeamMemberOrReadOnly
from .models import Team, Membership
from .serializers import TeamSerializer, TeamMembershipSerializer
from django_filters.rest_framework import DjangoFilterBackend


class TeamList(generics.ListCreateAPIView):
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
    # TeamDetails allows the user to delete or update their own teams   
    serializer_class = TeamSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Team.objects.all()


class TeamMembershipList(generics.ListCreateAPIView):
    # TeamMembershipList allows the user to join teams
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]    
    serializer_class = TeamMembershipSerializer   

    def get_queryset(self):
        return  Membership.objects.exclude(team__owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(member=self.request.user)


class TeamMates(generics.ListAPIView):
    # List of all members of all teams owned by the current user
    serializer_class = TeamMembershipSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Membership.objects.filter(team__owner=self.request.user)

class TeamMembershipDetails(generics.RetrieveDestroyAPIView):
    # TeamMembershipDetails allows users to leave teams
    serializer_class = TeamMembershipSerializer
    permission_classes = [IsTeamMemberOrReadOnly]

    def get_queryset(self):
        return  Membership.objects.all()
