from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import logging

from myfitapp.scripts import calculate_end_date, calories_finder

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

logger = logging.getLogger(__name__)


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
    protein = models.IntegerField()
    carbs = models.IntegerField()
    fats = models.IntegerField()
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField(blank=True, null=True)

    # Method to calculate the calorie budget for that day
    def calculate_calorie_budget(self):
        weight = float(self.profile.weight)
        goal = self.profile.goal
        if goal == "Lose":
            return round(weight * 2.202 * 13.5)
        elif goal == "Gain":
            return round(weight * 2.202 * 16)
        else:  # Maintain
            return round(weight * 2.202 * 15)

    # Method to calculate the macro nutrients required for an user
    def calculate_macros(self):
        calories = self.calorie_budget
        if self.profile.gender == "Male":
            protein = round(calories * 0.3) // 4
            carbs = round(calories * 0.5) // 4
            fats = round(calories * 0.2) // 9
        else:  # Female
            protein = round(calories * 0.25) // 4
            carbs = round(calories * 0.4) // 4
            fats = round(calories * 0.35) // 9

        # Adjust macros to match calorie budget
        total_calories = (protein * 4) + (carbs * 4) + (fats * 9)
        adjustment = (calories - total_calories) // 4
        carbs += adjustment  # Adjust carbs as a buffer

        return protein, carbs, fats

    def save(self, *args, **kwargs):
        if not self.start_date:
            self.start_date = timezone.now().date()
        logger.debug(f"Start Date: {self.start_date}")
        self.calorie_budget = self.calculate_calorie_budget()
        self.protein, self.carbs, self.fats = self.calculate_macros()
        self.end_date = calculate_end_date(self.start_date)
        """
        TODO: figure out this -> tried self.save() with different method name
          causing infinite recursion
        """
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
        """
        TODO: figure out this -> tried self.save() with different method name
          causing infinite recursion
        """
        super().save(*args, **kwargs)

    @staticmethod
    def daily_summary(profile):
        """
        this method will give a detailed summary about the food consumption
        on the day "Tracking Calories"
        """
        today = timezone.now().date()
        logs = UserFoodLog.objects.filter(profile=profile, date=today)

        total_calories = sum(log.calories for log in logs)
        total_protein = sum(log.protein_intake for log in logs)
        total_fats = sum(log.fat_intake for log in logs)
        total_carbs = sum(log.carbs_intake for log in logs)

        try:
            diet_plan = PersonalDietPlan.objects.get(profile=profile)
        except PersonalDietPlan.DoesNotExist:
            return {
                "error": "No diet plan available for this user.",
                "total_calories": total_calories,
                "total_protein": total_protein,
                "total_carbs": total_carbs,
                "total_fats": total_fats,
            }

        remaining_calories = max(diet_plan.calorie_budget - total_calories, 0)
        remaining_protein = max(diet_plan.protein - total_protein, 0)
        remaining_carbs = max(diet_plan.carbs - total_carbs, 0)
        remaining_fats = max(diet_plan.fats - total_fats, 0)

        return {
            "total_calories": total_calories,
            "remaining_calories": remaining_calories,
            "total_protein": total_protein,
            "remaining_protein": remaining_protein,
            "total_carbs": total_carbs,
            "remaining_carbs": remaining_carbs,
            "total_fats": total_fats,
            "remaining_fats": remaining_fats,
        }

    def __str__(self):
        return f"{self.profile.user.username} - {self.food_name} on {self.date}"


# Model to keep track of body metrics
class BodyMetrics(models.Model):
    """
    This is the model which will be used to keep track 
    of the user weight and goal changes
    """

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