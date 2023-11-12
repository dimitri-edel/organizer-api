""" Model classes of the team app """
# pylint: disable=R0903
# pylint: disable=no-member
# pylint: disable=no-name-in-module
from django.db import models
from django.contrib.auth.models import User
from organizer_api_prj.decorators import GetOrNoneManager


class Team(models.Model):
    """Team model class. Stores representations of teams"""

    # The user who created the team
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_owner")
    # The name of the team
    name = models.CharField(max_length=255, blank=False)

    class Meta:
        """Meta data"""

        ordering = ["name"]
        unique_together = ["owner", "name"]

    def __str__(self) -> str:
        return f"{self.name} created by {self.owner}"


class Membership(models.Model):
    """Membership model class. Stores team members of a certain Team"""

    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name="team_membership"
    )
    member = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="team_member"
    )

    objects = GetOrNoneManager()

    class Meta:
        """ " Meta data"""

        ordering = ["member"]
        unique_together = ["team", "member"]

    def __str__(self) -> str:
        return f" {self.member} is memeber of {self.team}"
