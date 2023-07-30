from django.db import models
from django.contrib.auth.models import User


class Team(models.Model):
    owner= models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_owner")
    name= models.CharField(max_length=255, blank=False)
    

    class Meta:
        ordering = ['name']
        unique_together = ['owner', 'name']

    def __str__(self) -> str:
        return f"{self.name} created by {self.owner}"


class Membership(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team_membership")
    member = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_member")

    class Meta:
        ordering = ['member']
        unique_together = ['team', 'member']

    def __str__(self) -> str:
        return f" {self.member} is memeber of {self.team}"
