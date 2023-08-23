""" Serializers for team app """
from rest_framework import serializers
from django.db import IntegrityError
from .models import Team, Membership

# pylint: disable=E1101


class TeamSerializer(serializers.ModelSerializer):
    """ Serializer for the Team objects """
    owner = serializers.ReadOnlyField(source="owner.username")
    is_member = serializers.SerializerMethodField()

    class Meta:
        """" Meta data """
        model = Team
        fields = [
            'id',
            'owner',
            'name',
            'is_member',
        ]

    def get_is_member(self, obj):
        """ Getter for is_member field """
        # The request object has been passed as a parameter to the constructor
        # in the views
        request = self.context['request']

        membership = Membership.objects.filter(team=obj, member=request.user)
        is_member = False
        if not membership:
            is_member = False
        else:
            is_member = True
        # Return True if the user is member of the given team
        return is_member

    def create(self, validated_data):
        # Prevent duplicate likes
        try:
            return super().create(validated_data)
        except IntegrityError as exc:
            # Due to models.Team.unique_together['owner', 'name]
            # if the user attmpts to add a team twice an IntegrityError will be rasied
            raise serializers.ValidationError({
                'detail': 'Cannot create the same team twice!'
            }) from exc


class TeamMembershipSerializer(serializers.ModelSerializer):
    """ Serializer for Membership objects """
    user_id = serializers.ReadOnlyField(source="member.id")
    member = serializers.ReadOnlyField(source="member.username")
    team_name = serializers.ReadOnlyField(source="team.name")

    class Meta:
        """ Meta data """
        model = Membership
        fields = [
            'id',
            'team_name',
            'team',
            'user_id',
            'member',
        ]

    def create(self, validated_data):
        # Prevent duplicate Memberships
        try:
            return super().create(validated_data)
        except IntegrityError as exc:
            # Due to models.Memebership.unique_together['team', 'memeber']
            # if the user attmpts to add a team twice an IntegrityError will be rasied
            raise serializers.ValidationError({
                'detail': 'Cannot create the same team twice!'
            }) from exc
