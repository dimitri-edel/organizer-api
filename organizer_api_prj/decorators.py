"""Decorators for standard library elements"""
# pylint: disable=too-few-public-methods
from django.db import models


class GetOrNoneManager(models.Manager):
    """
    This class inherits from the standard model manager.
    It extends the Manager by one method get_or_none.
    It becomes handy if it is necessary to get a None instead of having the
    model throw an exception, as it would if one uses objects.get()
    """

    def get_or_none(self, **kwargs):
        """Return None if the query there is no matching query"""
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None
