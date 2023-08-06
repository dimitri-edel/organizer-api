from django.db import models
from django.contrib.auth.models import User
from team.models import Membership
from django.core.validators import FileExtensionValidator

CATEGORY = ((0, "Chore"),(1, "Errand"), (2, "Work"))
PRIORITY = ((0,"High"), (1, "Middle"), (2, "Low"))
STATUS = ((0,"Open"), (1, "Progressing"), (2, "Done"))

class Task(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="task_owner")
    asigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True ,related_name="task_asigned_to")
    name = models.CharField(max_length=200, blank=False)
    due_date = models.DateTimeField(auto_now_add=True)
    category = models.IntegerField(choices=CATEGORY, default=0)
    priority = models.IntegerField(choices=PRIORITY, default=0)
    status = models.IntegerField(choices=STATUS, default=0)
    file = models.FileField(upload_to="media/", null=True, validators=[FileExtensionValidator(allowed_extensions=["jpg", "png", "webp", "bmp"])])

    class Meta:
        ordering = ['-due_date']


