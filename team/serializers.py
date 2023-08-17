from rest_framework import serializers
from .models import Team, Membership
from django.db import IntegrityError


class TeamSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    is_member = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            'id',
            'owner',
            'name',
            'is_member',
        ]

    def get_is_member(self, obj):
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