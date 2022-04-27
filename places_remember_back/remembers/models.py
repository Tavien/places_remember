from users.models import User
from django.contrib.gis.db import models

"""
new comment
"""

class RemembersModel(models.Model):
    """
    Memory container model class
    """
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=600)
    location_point = models.PointField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}: {self.name}'
