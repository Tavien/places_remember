from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    User class overload, photo field added
    """
    photo = models.URLField(blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.username})'
