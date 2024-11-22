from django.db import models
from django.contrib.auth.models import User

from .scripts import calories_finder

# Global Variables
LEVEL_CHOICES = [
    ("Beginner", "Beginner"),
    ("Intermediate", "Intermediate"),
    ("Advance", "Advance"),
]
GENDER_CHOICES = [("M", "Male"), ("F", "Female")]
GOAL_CHOICES = [
    ("Lose", "Lose Weight"),
    ("Gain", "Gain Weight"),
    ("Maintain", "Maintain Weight"),
]


# Model for storing user profile information
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # in kg
    height = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )  # in cm
    current_level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    body_fat_percentage = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES)

    def __str__(self):
        return self.user.username


# Muscle Group Model
class MuscleGroup(models.Model):
    name = models.CharField()

    def __str__(self):
        return self.name


# Current Fitness Level Model
class TrainingLevel(models.Model):
    current_level = models.CharField(max_length=20, choices=LEVEL_CHOICES)

    def __str__(self):
        return self.current_level


# Resistance Training Model
class ResistanceTraining(models.Model):
    exercise_name = models.CharField(max_length=50)
    sets = models.CharField(max_length=50)
    reps = models.CharField(max_length=50)
    weight = models.CharField(max_length=500)  # in kg
    muscle_group = models.ForeignKey(
        MuscleGroup, on_delete=models.CASCADE, related_name="resistance"
    )
    current_level = models.ForeignKey(
        TrainingLevel, on_delete=models.CASCADE, related_name="resistance"
    )

    def __str__(self):
        return f"{self.exercise_name} - Sets: {self.sets}, Reps: {self.reps}"


# Cardio Training Model
class CardioTraining(models.Model):
    exercise_name = models.CharField(max_length=50)
    duration = models.PositiveIntegerField()  # in minutes
    intensity = models.CharField(
        max_length=20,
        choices=[("Low", "Low"), ("Moderate", "Moderate"), ("High", "High")],
    )
    current_level = models.ForeignKey(
        TrainingLevel, on_delete=models.CASCADE, related_name="cardio"
    )

    def __str__(self):
        return f"{self.exercise_name} - Duration: {self.duration} mins, Intensity: {self.intensity}"


# CrossFit Training Model
class CrossFitTraining(models.Model):
    exercise_name = models.CharField(max_length=50)
    rounds = models.PositiveIntegerField()
    time_cap = models.PositiveIntegerField(null=True, blank=True)  # in minutes
    current_level = models.ForeignKey(
        TrainingLevel, on_delete=models.CASCADE, related_name="crossfit"
    )

    def __str__(self):
        return f"{self.exercise_name} - Rounds: {self.rounds}"


# Flexibility Training Model
class FlexibilityTraining(models.Model):
    exercise_name = models.CharField(max_length=50)
    duration = models.PositiveIntegerField()  # in seconds or minutes
    stretch_type = models.CharField(
        max_length=20, choices=[("Static", "Static"), ("Dynamic", "Dynamic")]
    )

    def __str__(self):
        return f"{self.exercise_name} - {self.stretch_type} Stretch"


# Recovery Model
class Recovery(models.Model):
    method_name = models.CharField(max_length=50)
    duration = models.PositiveIntegerField(null=True, blank=True)  # in minutes
    recovery_type = models.CharField(
        max_length=20,
        choices=[
            ("Active", "Active"),
            ("Passive", "Passive"),
            ("Psychological", "Psychological"),
        ],
    )

    def __str__(self):
        return f"{self.method_name} - {self.recovery_type} Recovery"


# Model for storing a personalized workout plan for a user
class PersonalWorkoutPlan(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="workout_plans"
    )
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)
    resistance_trainings = models.ManyToManyField(ResistanceTraining, blank=True)
    cardio_trainings = models.ManyToManyField(CardioTraining, blank=True)
    crossfit_trainings = models.ManyToManyField(CrossFitTraining, blank=True)
    flexibility_trainings = models.ManyToManyField(FlexibilityTraining, blank=True)
    recoveries = models.ManyToManyField(Recovery, blank=True)

    def __str__(self):
        return f"{self.profile.user.username} - Workout Plan"


# Model for storing a personalized diet plan for a user
class PersonalDietPlan(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    calorie_budget = models.IntegerField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    def calculate_calorie_budget(self):
        weight = self.profile.weight
        goal = self.profile.goal
        if goal == "Lose":
            return round(weight * 2.202 * 13.5)
        elif goal == "Gain":
            return round(weight * 2.202 * 16)
        else:  # Maintain
            return round(weight * 2.202 * 15)

    def save(self, *args, **kwargs):
        self.calorie_budget = self.calculate_calorie_budget()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.profile.user.username} - Diet Plan"


# Model to log food intake for a user
class UserFoodLog(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="food_logs"
    )
    food_name = models.CharField(max_length=255, default="unknown")
    quantity = models.PositiveIntegerField()  # e.g., grams, servings
    calories = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    protein_intake = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    fat_intake = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    carbs_intake = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):  # Overriding the save()
        nutrition = calories_finder(self.food_name, self.quantity)

        self.calories = nutrition["calories"]
        self.protein_intake = nutrition["protein_g"]
        self.carbs_intake = nutrition["carbohydrates_total_g"]
        self.fat_intake = nutrition["fat_total_g"]

        super().save()

    def __str__(self):
        return f"{self.profile.user.username} - {self.food_name} on {self.date}"


# Model to keep track of body metrics
class BodyMetrics(models.Model):
    profile = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="body_metrics"
    )
    date = models.DateField(auto_now_add=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2)  # in kg
    body_fat_percentage = models.DecimalField(
        max_digits=4, decimal_places=1, null=True, blank=True
    )

    def __str__(self):
        return f"{self.profile.user.username} - {self.date}"