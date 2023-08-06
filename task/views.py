from rest_framework import generics
from organizer_api_prj.permissions import IsOwnerOrTeamMemberOrReadOnly
from rest_framework.permissions import IsAuthenticated
from .seritalizers import TaskSerializer
from .models import Task
from django.db.models import Q



class TaskList(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user_id = self.request.user.id
        # if the user is not logged in
        if user_id is None:
            # return an empty list
            return Task.objects.none()
        # else deliver a list of tasks owned by the user, or assigned to the user        
        else:            
            return Task.objects.filter(Q(owner=self.request.user) | Q(asigned_to=self.request.user))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrTeamMemberOrReadOnly]
    queryset=Task.objects.all()