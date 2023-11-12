""" Serializers for team app """
# pylint: disable=E1101
# pylint: disable=too-few-public-methods
# pylint: disable=E0611

from rest_framework import serializers
from .models import PrivateMessage


class PrivateMessageSerializer(serializers.ModelSerializer):
    """
    Data serializer of PrivateMessage objects for HTML Response objects.
    """

    # Ensure that the owner cannot be altered. And the HTML Response returns the
    # name of the user
    owner = serializers.ReadOnlyField(source="owner.username")
    ## Ensure that the recipient cannot be altered
    recipient = serializers.ReadOnlyField(source="recipient.username")

    def update(self, instance, validated_data):
        """Override the update method to meet the update requirements"""

        instance.message = validated_data.get("message")

        if validated_data.get("image"):
            instance.image = validated_data.get("image")

        instance.save()
        return instance

    class Meta:
        """Meta data for the model serialization"""

        # The model that will be serialized
        model = PrivateMessage
        # The fields in the model that will be serialized
        fields = [
            "id",
            "team",
            "owner",
            "recipient",
            "message",
            "created_at",
            "image",
        ]
