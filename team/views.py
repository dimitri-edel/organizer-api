from rest_framework import generics, permissions
from .models import Team
from .serializers import TeamSerializer


class TeamList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TeamDetails(generics.RetrieveDestroyAPIView):    
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    queryset = Team.objects.all()
