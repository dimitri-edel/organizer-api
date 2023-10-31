""" Views for the team chat room """
# pylint: disable=E1101
# pylint: disable=unused-argument
# pylint: disable=E0611

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics, filters

# from rest_framework.permissions import IsAuthenticatedOrReadOnly

# from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from organizer_api_prj.permissions import (
    IsTeamAccessAuthorized,
    IsTeamChatMessageOwner,
    IsOwnerOrTeamMemberOrReadOnly,
)
from team.models import Team
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
        username = request.GET.get("username")
        # Get the entire set messages for the requested team
        messages = TeamMessage.objects.filter(team=team)

        if username is not None:
            owner = User.objects.get(username=username)
            # Filter the set of messages by user
            messages = messages.filter(owner=owner)
        # print(f"owner={owner.username}")
        serializer = TeamMessageSerializer(
            messages, many=True, context={"request": request}
        )
        return Response(serializer.data)


class TeamChatPost(APIView):
    """View for posting messages in a team chat

    Args:
        APIView (APIView): DRF view that supports all the  types of requests

    Returns:
        HTTP Response: If the posted data was valid, the response status will
        be 201 for CREATED and the response data will contain the JSON object
        with the created dataset
    """

    # Data serializer for the class TeamMessage
    serializer_class = TeamMessageSerializer
    # The class that holds permissions to the team chat for users
    permission_classes = [IsTeamAccessAuthorized]

    def post(self, request, team_id):
        """Process the POST request

        Args:
            request (HTTP request): The request from the client
            team_id (Integer): The private key of the team, which
            the write request is referring to. Even though, the
            team-id is also part of the submitted form, I made it
            part of the URL route, so I do not have to create a
            separate permission class. Meaning that the permission
            class uses the team_id parameter of a view class to
            determine if the user requesting access is allowed to
            do so.
            IMPORTANT: The team-id that is sent in a HTML-form
            or a JSON-object, will be overwritten inside this
            method to match the requested team in the URL route.

        Returns:
            HTTP Response: If the posted data was valid, the response status will
        be 201 for CREATED and the response data will contain the JSON object
        with the created dataset
        """
        serializer = TeamMessageSerializer(
            data=request.data, context={"request": request}
        )
        # Retrieve the respective team object
        team = Team.objects.get(id=team_id)

        if serializer.is_valid():
            serializer.save(owner=request.user, team=team)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamChatPut(APIView):
    """View for updating messages in a team chat

    Args:
        APIView (APIView): DRF view that supports all the  types of requests

    Returns:
        HTTP Response: If the posted data was valid, the response status will
        be 200 for OK and the response data will contain the JSON object
        with the updated fields
    """

    # Data serializer for the class TeamMessage
    serializer_class = TeamMessageSerializer
    # The permission class that determines whether or not
    # the user requesting to update the message is its owner
    permission_classes = [IsTeamChatMessageOwner]

    def put(self, request, message_id):
        """Process the PUT request

        Args:
            request (HTTP request): The request from the client
            message_id (Integer): The private key of the message, which
            the write request is referring to.

        Returns:
            HTTP Response: If the posted data was valid, the response status will
        be 200 for OK and the response data will contain the JSON object
        with the updated dataset
        """

        # Get the instance of the message
        message = TeamMessage.objects.get(id=message_id)

        serializer = TeamMessageSerializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            serializer.update(instance=message, validated_data=request.data)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeamChatDelete(APIView):
    """View for deleting messages in a team chat

    Args:
        APIView (APIView): DRF view that supports all the  types of requests

    Returns:
        HTTP Response: If the deletion was successful, the response status will
        be 200 for OK and the response data will contain the JSON object
        with the deleted object
    """

    # Data serializer for the class TeamMessage
    serializer_class = TeamMessageSerializer
    # The permission class that determines whether or not
    # the user requesting to update the message is its owner
    permission_classes = [IsTeamChatMessageOwner]

    def delete(self, request, message_id):
        """Process the DELETE request

        Args:
            request (HTTP request): The request from the client
            message_id (Integer): The private key of the message, which
            the write request is referring to.

        Returns:
            HTTP Response: If the posted data was valid, the response status will
        be 200 for OK and the response data will contain the JSON object
        with the updated dataset
        """

        # Get the instance of the message and delete it
        message = TeamMessage.objects.get(id=message_id).delete()
        # If the deletion was a success, then return the OK status
        # and a serialized tuple that indicates the number of objects
        # that have been deleted and also contains the type of the object
        # which is team_chat.TeamMessage
        if message is not None:
            return Response(message, status=status.HTTP_200_OK)
        # Return a bad request if the deletion did not succeed
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TeamChatList(generics.ListAPIView):
    """
    This generic view allows users to view messages of in the chat
    or post new messages
    """

    model = TeamMessage
    # Only allow users who are members of the team or their
    # owners to create and view the messages
    permission_classes = [IsOwnerOrTeamMemberOrReadOnly]
    # The serializer of the model objects for HTML Response objects
    serializer_class = TeamMessageSerializer
    # Retrieve all messages that are permitted to the user
    # queryset = TeamMessage.objects.all()
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
    ]
    # fields for SearchFilter
    search_fields = [
        "owner__username",
    ]
    # fields for DjangoFilterBackend
    filterset_fields = [
        "owner__username",
    ]

    # def perform_create(self, serializer):
    #     """Method for posting a new message in the team chat room"""
    #     serializer.save(owner=self.request.user)

    def get_queryset(self):
        team_id = self.request.GET.get("team_id")
        if team_id is None:
            return TeamMessage.objects.none()

        team = Team.objects.get(id=team_id)

        messages = TeamMessage.objects.filter(team=team)

        return messages
