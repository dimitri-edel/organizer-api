from rest_framework import serializers
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username') 
    
    class Meta:
        model = Task
        fields = [
            'id',
            'owner',
            'asigned_to',
            'title',
            'comment',
            'due_date',
            'category',
            'priority',
            'status',
            'file',
        ]