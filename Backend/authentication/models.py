from django.db import models
from django.contrib.auth.models import User

from myfitapp.choices import GenderChoices, LevelChoices, GoalChoices


# Model for storing user profile information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=1, choices=GenderChoices.choices, default=GenderChoices.MALE
    )
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # in kg
    height = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )  # in cm
    current_level = models.CharField(
        max_length=20, choices=LevelChoices.choices, default=LevelChoices.BEGINNER
    )
    body_fat_percentage = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    goal = models.CharField(
        max_length=10, choices=GoalChoices.choices, default=GoalChoices.MAINTAIN
    )

    def __str__(self):
        return self.user.username
