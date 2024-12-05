from rest_framework import serializers

from myfitapp.choices import LevelChoices
from myfitapp.models import (
    CardioTraining,
    CrossFitTraining,
    UserFoodLog,
    FlexibilityTraining,
    MuscleGroup,
    PersonalDietPlan,
    PersonalWorkoutPlan,
    Recovery,
    ResistanceTraining,
)


# Serializer for certain Muscle Group
class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = ["id", "name"]


# Serializers for Workouts and Physical activities
class ResistanceTrainingSerializer(serializers.ModelSerializer):
    muscle_group = MuscleGroupSerializer()

    class Meta:
        model = ResistanceTraining
        fields = [
            "id",
            "exercise_name",
            "sets",
            "reps",
            "muscle_group",
            "current_level",
        ]


# Serializer for Cardio
class CardioTrainingSerializer(serializers.ModelSerializer):

    class Meta:
        model = CardioTraining
        fields = ["id", "exercise_name", "duration", "intensity", "current_level"]


# Serializer for cardio
class CrossFitTrainingSerializer(serializers.ModelSerializer):

    class Meta:
        model = CrossFitTraining
        fields = ["id", "exercise_name", "rounds", "time_cap", "current_level"]


# Serializer for flexibility
class FlexibilityTrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlexibilityTraining
        fields = "__all__"


# Serializer for Recovery
class RecoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = Recovery
        fields = "__all__"


# Serializer to log food
class UserFoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFoodLog
        fields = [
            "id",
            "food_name",
            "quantity",
            "calories",
            "protein_intake",
            "carbs_intake",
            "fat_intake",
            "date",
        ]
        read_only_fields = [
            "calories",
            "protein_intake",
            "fat_intake",
            "carbs_intake",
            "date",
        ]


# Serializer for personal workouts
class PersonalWorkoutPlanSerializer(serializers.ModelSerializer):
    level = serializers.ChoiceField(
        choices=LevelChoices.choices,
        write_only=True,
        help_text="Specify the level of workouts (Beginner, Intermediate, Advanced)",
    )
    workout_type = serializers.ChoiceField(
        choices=[
            ("Resistance", "Resistance"),
            ("Cardio", "Cardio"),
            ("CrossFit", "CrossFit"),
            ("Flexibility", "Flexibility"),
            ("Recovery", "Recovery"),
        ],
        write_only=True,
        help_text="Specify the type of workout to include in the plan",
    )

    crossfit_trainings = CrossFitTrainingSerializer(many=True, read_only=True)
    resistance_trainings = ResistanceTrainingSerializer(many=True, read_only=True)
    cardio_trainings = CardioTrainingSerializer(many=True, read_only=True)
    flexibility_trainings = FlexibilityTrainingSerializer(many=True, read_only=True)
    recoveries = RecoverySerializer(many=True, read_only=True)

    class Meta:
        model = PersonalWorkoutPlan
        fields = [
            "profile",
            "start_date",
            "end_date",
            "level",
            "workout_type",
            "resistance_trainings",
            "cardio_trainings",
            "crossfit_trainings",
            "flexibility_trainings",
            "recoveries",
        ]
        extra_kwargs = {
            "profile": {"read_only": True},
            "start_date": {"required": False},
            "end_date": {"required": False},
        }

    def create(self, validated_data):
        level = validated_data.pop("level")
        workout_type = validated_data.pop("workout_type")

        validated_data["profile"] = self.context["request"].user.profile

        workout_plan = PersonalWorkoutPlan.objects.create(**validated_data)

        workout_mapping = {
            "Resistance": ("resistance_trainings", ResistanceTraining.objects.filter(current_level=level)),
            "Cardio": ("cardio_trainings", CardioTraining.objects.filter(current_level=level)),
            "CrossFit": ("crossfit_trainings", CrossFitTraining.objects.filter(current_level=level)),
            "Flexibility": ("flexibility_trainings", FlexibilityTraining.objects.filter(current_level=level)),
            "Recovery": ("recoveries", Recovery.objects.filter(current_level=level)),
        }

        field_name, workouts = workout_mapping.get(workout_type, (None, None))

        if workouts.exists():
            existing_workouts = getattr(workout_plan, field_name).all()
            new_workouts = workouts.exclude(id__in=existing_workouts.values_list("id", flat=True))

            getattr(workout_plan, field_name).set(new_workouts)
        else:
            raise serializers.ValidationError(
                f"No {workout_type} workouts found for level {level}."
            )

        return workout_plan

    def to_representation(self, instance):

        data = super().to_representation(instance)
        workout_fields = [
            "resistance_trainings",
            "cardio_trainings",
            "crossfit_trainings",
            "flexibility_trainings",
            "recoveries",
        ]

        # Remove empty workout fields from the representation
        for field in workout_fields:
            if not data.get(field):
                data.pop(field)

        return data


# Serializer for personal diet plan
class PersonalDietPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonalDietPlan
        fields = [
            "profile",
            "calorie_budget",
            "protein",
            "carbs",
            "fats",
            "start_date",
            "end_date",
        ]
        read_only_fields = ["calorie_budget", "protein", "carbs", "fats", "start_date"]

    def validate(self, data):
        profile = data.get("profile")

        if not profile.weight or profile.weight <= 0:
            raise serializers.ValidationError("Profile must have a valid weight.")
        if not profile.goal:
            raise serializers.ValidationError(
                "Profile must have a valid goal (Lose, Gain, Maintain)."
            )
        if not profile.gender:
            raise serializers.ValidationError(
                "Profile must have a valid gender (Male or Female)."
            )

        return data

    def create(self, validated_data):
        profile = validated_data["profile"]

        # Create an instance of the model without saving
        diet_plan = PersonalDietPlan(profile=profile)

        # Calculate calorie budget and macros
        diet_plan.calorie_budget = diet_plan.calculate_calorie_budget()
        diet_plan.protein, diet_plan.carbs, diet_plan.fats = (
            diet_plan.calculate_macros()
        )

        # Save the instance with calculated fields
        diet_plan.save()
        return diet_plan


# Serializer for searching a food for nutritional information
class SearchSerializer(serializers.Serializer):
    food_name = serializers.CharField()
    quantity = serializers.IntegerField()  # in grams


# Serializer for searching a food for recipe
class RecipeSerializer(serializers.Serializer):
    food_name = serializers.CharField()
