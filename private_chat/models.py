""""Model for the messages in the team chat room"""
# pylint: disable=no-name-in-module
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.db import models
from organizer_api_prj.decorators import GetOrNoneManager
from team.models import Team


class PrivateMessage(models.Model):
    """Model for messages in the private team chat"""

    # The team that the message belongs to
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="team_private_message"
    )
    # The user who posted the message
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="private_message_owner"
    )
    # The recipient of the message
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="private_message_recipient"
    )
    # The text message
    message = models.TextField()
    # Timestamp of the day and time when the message was posted
    created_at = models.DateTimeField(auto_now_add=True)
    # An optional image attached to the message
    image = models.FileField(
        upload_to="media/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png", "webp", "bmp"])
        ],
    )
    # Decorator for returning None instead of throwing an exception
    objects = GetOrNoneManager()

    class Meta:
        """Meta information for the model"""

        # order messages by the date and time they were created in ascending order
        ordering = ["created_at"]
