from rest_framework import serializers
from .models import Team
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