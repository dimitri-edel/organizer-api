""" Serializers for team app """
# pylint: disable=E1101
# pylint: disable=too-few-public-methods
# pylint: disable=E0611

from rest_framework import serializers
from .models import TeamMessage


class TeamMessageSerializer(serializers.ModelSerializer):
    """
    Data serializer of TeamMessage objects for HTML Response objects.
    """

    # Ensure that the owner cannot be altered. And the HTML Response returns the
    # name of the user
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        """Meta data for the model serialization"""

        # The model that will be serialized
        model = TeamMessage
        # The fields in the model that will be serialized
        fields = [
            "id",
            "team",
            "owner",
            "message",
            "created_at",
            "image",
        ]
