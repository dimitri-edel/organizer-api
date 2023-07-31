from rest_framework import generics
from organizer_api_prj.permissions import IsOwnerOrTeamMemberOrReadOnly
from .seritalizers import TaskSerializer
from .models import Task

class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrTeamMemberOrReadOnly]
    queryset=Task.objects.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        