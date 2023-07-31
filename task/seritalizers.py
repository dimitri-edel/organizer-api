from rest_framework import serializers
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    file = serializers.ReadOnlyField(source='file.url')
    asigned_to = serializers.ReadOnlyField(source='asigned_to.username')
    # asigned_to = models.ForeignKey(
    #     Membership.member, on_delete=models.CASCADE, related_name="task_asigned_to")
    # name = models.CharField(max_length=200, blank=False)
    # due_date = models.DateTimeField(auto_now_add=True)
    # category = models.IntegerField(choices=CATEGORY, default=0)
    # priority = models.IntegerField(choices=PRIORITY, default=0)
    # status = models.IntegerField(choices=STATUS, default=0)
    # file = models.FileField(upload_to="media/")

    class Meta:
        model = Task
        fields = [
            'id',
            'owner',
            'asigned_to',
            'name',
            'due_date',
            'category',
            'priority',
            'status',
            'file',
        ]