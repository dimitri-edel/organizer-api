""" Views for Task Model """
from rest_framework import generics, filters
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from organizer_api_prj.permissions import IsOwnerOrTeamMemberOrReadOnly
from .seritalizers import TaskSerializer
from .models import Task

# pylint: disable=E1101


class TaskList(generics.ListCreateAPIView):
    """ View for generating a Task List for
        Users and creating a new Task
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    # fields for SearchFilter
    search_fields = [
        'owner__username',
        'title',
        'due_date',
        'category',
        'priority',
        'status',
    ]
    # fields for OrderingFilter
    ordering_fields = [
        'due_date',        
        'priority',
        'status',
    ]
    # fields for DjangoFilterBackend
    filterset_fields = [
        'owner',
        'due_date',
        'category',
        'priority',
        'status',
    ]
    
    def get_queryset(self):
        """ override the queryset """
        user_id = self.request.user.id
        # if the user is not logged in
        if user_id is None:
            # return an empty list
            return Task.objects.none()
        # else deliver a list of tasks owned by the user, or assigned to the user
        return Task.objects.filter(Q(owner=self.request.user) | Q(asigned_to=self.request.user))

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TaskDetails(generics.RetrieveUpdateDestroyAPIView):
    """ View for updating, deleting or retrieving a paritcular Task"""
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrTeamMemberOrReadOnly]
    queryset=Task.objects.all()
