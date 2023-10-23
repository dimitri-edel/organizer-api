""" Views for the team chat room """
# pylint: disable=E1101
# pylint: disable=unused-argument
# pylint: disable=E0611

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# from rest_framework import generics, filters
# from rest_framework.permissions import IsAuthenticatedOrReadOnly

# from django.db.models import Q
# from django_filters.rest_framework import DjangoFilterBackend
from organizer_api_prj.permissions import IsTeamAccessAuthorized
from team.models import Team, Membership
from .serializers import TeamMessageSerializer
from .models import TeamMessage


class TeamChat(APIView):
    """View for retrieving messages in a team chat room

    Args:
        APIView (View): Provides an APIView class that is the base of all views in REST framework.

    """

    # Data serializer for the class TeamMessage
    serializer_class = TeamMessageSerializer
    # The class that holds permissions to the team chat for users
    permission_classes = [IsTeamAccessAuthorized]

    def get(self, request, team_id):
        """Process the GET request

        Args:
            request (GET-Request): The GET request sent by the client
            team_id (Integer): The PK of the requested team

        Returns:
            Serialized JSON: List of messages in the respective team chat
        """
        team = Team.objects.get(id=team_id)

        teams = TeamMessage.objects.filter(team=team)
        serializer = TeamMessageSerializer(
            teams, many=True, context={"request": request}
        )
        return Response(serializer.data)


# class TeamChatPost(APIView):
#     """View for posting messages in a team chat

#     Args:
#         APIView (APIView): DRF view that supports all the  types of requests

#     Returns:
#         HTTP Response: If the posted data was valid, the response status will
#         be 201 for CREATED and the response data will contain the JSON object
#         with the created dataset
#     """

#     serializer_class = TeamMessageSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]

#     def post(self, request):
#         """Process the POST request

#         Args:
#             request (HTTP request): The request from the client

#         Returns:
#             HTTP Response: If the posted data was valid, the response status will
#         be 201 for CREATED and the response data will contain the JSON object
#         with the created dataset
#         """
#         serializer = TeamMessageSerializer(
#             data=request.data, context={"request": request}
#         )

#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def check_auth(self, team, user):
#         """
#         Check if the user requesting the list of entries in the chat room
#         is permitted to do it.
#         The user is allowed to make this request if they are either a member
#         of the team or if they are the owner of the team.
#         """
#         # See if the user is member of the requested team
#         membership = Membership.objects.get(team=team, member_id=user.id)
#         # See if the user if the owner of the team
#         team_owner = team.owner is user

#         # If the user is neither the owner of the team nor a member,
#         # deny access
#         if not membership and not team_owner:
#             return False
#         # Otherwise grant access
#         return True


# class TeamChat(generics.ListCreateAPIView):
#     """
#     This generic view allows users to view messages of in the chat
#     or post new messages
#     """

#     # Only allow users who are members of the team or their
#     # owners to create and view the messages
#     permission_classes = [IsOwnerOrTeamMemberOrReadOnly]
#     # The serializer of the model objects for HTML Response objects
#     serializer_class = TeamMessageSerializer
#     # Retrieve all messages that are permitted to the user
#     queryset = TeamMessage.objects.all()

#     def perform_create(self, serializer):
#         """Method for posting a new message in the team chat room"""
#         serializer.save(owner=self.request.user)
