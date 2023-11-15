""" Model class for Task """
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

CATEGORY = ((0, "Chore"), (1, "Errand"), (2, "Work"))
PRIORITY = ((0, "High"), (1, "Middle"), (2, "Low"))
STATUS = ((0, "Open"), (1, "Progressing"), (2, "Done"))


class Task(models.Model):
    """Representation of a single Task in the database"""

    # User who owns a given Task
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_owner")
    # User who is assigned to a given task. This field must not be assigned.
    asigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="task_asigned_to",
    )
    # Title of a given Task
    title = models.CharField(max_length=200, blank=False)
    # Comments
    comment = models.TextField(blank=True, default="")
    # Date and time of when the task is due
    due_date = models.DateTimeField()
    category = models.IntegerField(choices=CATEGORY, default=0)
    priority = models.IntegerField(choices=PRIORITY, default=0)
    status = models.IntegerField(choices=STATUS, default=0)
    # File that is attached to the task. A file uploaded can only be
    # of the specified format (JPG, PNG, WEBP, BMP)
    file = models.FileField(
        upload_to="media/",
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png", "webp", "bmp"])
        ],
    )

    class Meta:
        """Meta data"""

        ordering = ["-due_date"]
