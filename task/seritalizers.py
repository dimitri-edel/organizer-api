from rest_framework import serializers
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') 
    is_owner = serializers.SerializerMethodField()
    asigned_to_username = serializers.ReadOnlyField(source='asigned_to.user.username')

    def get_is_owner(self, obj):
        # The request object has been passed as a parameter to the constructor
        # in the views
        request = self.context['request']
        # Return True if the user is the owner of the object
        return request.user == obj.owner


    class Meta:
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