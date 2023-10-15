""""Model for the messages in the team chat room"""
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User
from django.db import models
from team.models import Team


class TeamMessage(models.Model):
    """Model for messages in the team chat"""

    # The team that the message belongs to
    task = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_chat")
    # The user who posted the message
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="team_message_owner"
    )
    # The text message
    message = models.TextField()
    # An optional image attached to the message
    image = models.FileField(
        upload_to="media/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png", "webp", "bmp"])
        ],
    )
