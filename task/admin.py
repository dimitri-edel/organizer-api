from django.contrib import admin
from .models import Task
from team.models import Team, Membership

# Register your models here.
admin.site.register(Task)
admin.site.register(Team)
admin.site.register(Membership)
