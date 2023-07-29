from rest_framework import serializers
from .models import Team, Membership
from django.db import IntegrityError


class TeamSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Team
        fields = [
            'id',
            'owner',
            'name',
        ]


    def create(self, validated_data):
    # Prevent duplicate likes
        try:
            return super().create(validated_data)
        except IntegrityError:
        # Due to models.Team.unique_together['owner', 'name]
        # if the user attmpts to add a team twice an IntegrityError will be rasied        
            raise serializers.ValidationError({
                'detail': 'Cannot create the same team twice!'
            })


class TeamMembershipSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source="member.id")
    member = serializers.ReadOnlyField(source="member.username")
    team_id = serializers.ReadOnlyField(source="team.id")
    # team = serializers.CharField(source="team.name")

    class Meta:
        model = Membership
        fields = [
            'id',
            'team_id',
            'team',
            'user_id',
            'member',
        ]


    def create(self, validated_data):
    # Prevent duplicate likes
        try:
            return super().create(validated_data)
        except IntegrityError:
        # Due to models.Team.unique_together['team', 'memeber']
        # if the user attmpts to add a team twice an IntegrityError will be rasied        
            raise serializers.ValidationError({
                'detail': 'Cannot create the same team twice!'
            })