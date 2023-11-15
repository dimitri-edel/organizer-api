""" Views for the team chat room """
# pylint: disable=E1101
# pylint: disable=unused-argument
# pylint: disable=E0611

from datetime import timedelta, datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from organizer_api_prj.permissions import (
    IsTeamAccessAuthorized,
    IsTeamChatMessageOwner,
    IsOwnerOrTeamMemberOrReadOnly,
)
from team.models import Team
from .serializers import TeamMessageSerializer
from .models import TeamMessage


class TeamChatMessageCount(APIView):
    """View for retrieving messages in a team chat room

    Args:
        APIView (View): Provides an APIView class that is the base of all views in REST framework.

    """

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
        # username = request.GET.get("username")
        # Get the entire set messages for the requested team
        messages = TeamMessage.objects.filter(team=team)
        # Count the messages
        count = messages.count()
        # Return a dictionary with the number of messages found
        return Response({"count": count})


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

        # Get the instance of the message or a None object if there is
        # no such message
        message = TeamMessage.objects.get_or_none(id=message_id)
        # If the deletion was a success, then return the OK status
        if message is not None:
            message.delete()
            return Response({"details: message deleted!"}, status=status.HTTP_200_OK)
        # Signal that the message was not found
        return Response(status=status.HTTP_404_NOT_FOUND)


class TeamChatList(generics.ListAPIView):
    """
    This generic view allows users to view messages of in the chat
    or post new messages
    Filters: search - allows to filter the messages by the
    username of the user who posted them or the text in the message
    Pagination parameters: limit, offset, page
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
        "message",
    ]
    # fields for DjangoFilterBackend
    filterset_fields = [
        "owner__username",
    ]

    def get_queryset(self):
        # Extract GET parameter named team_id &team_id=?
        team_id = self.request.GET.get("team_id")
        # Extract GET parameter named minus_days &minus_days=?
        minus_days = self.request.GET.get("minus_days")
        if team_id is None:
            return TeamMessage.objects.none()

        team = Team.objects.get_or_none(id=team_id)

        messages = TeamMessage.objects.filter(team=team)

        # If minus_days parameter exists and has a valid value
        if minus_days is not None and int(minus_days) > 0:
            # Filter the messages to only contain messages
            # that are older than minus_days
            # In layman terms, if minus_days equals to 5
            # then the query will only return the messages
            # posted in the last 5 days
            messages = messages.filter(
                created_at__gte=(datetime.now() - timedelta(days=int(minus_days)))
            )
        return messages
