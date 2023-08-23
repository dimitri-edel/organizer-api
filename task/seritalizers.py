""" Data Serializer for the Task objects """
from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    """ Serializer for Task objects """
    owner = serializers.ReadOnlyField(source='owner.username')
    is_owner = serializers.SerializerMethodField()
    asigned_to_username = serializers.ReadOnlyField(
        source='asigned_to.username')

    def get_is_owner(self, obj):
        """ override getter for the is_owner field."""
        # The request object has been passed as a parameter to the constructor
        # in the views
        request = self.context['request']
        # Return True if the user is the owner of the object
        return request.user == obj.owner

    class Meta:
        """ Meta data """
        model = Task
        fields = [
            'id',
            'owner',
            'is_owner',
            'asigned_to',
            'asigned_to_username',
            'title',
            'comment',
            'due_date',
            'category',
            'priority',
            'status',
            'file',
        ]
