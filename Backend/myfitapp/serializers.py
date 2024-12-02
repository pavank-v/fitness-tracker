from rest_framework import serializers
from django.contrib.auth.models import User
from myfitapp.models import (BodyMetrics, CardioTraining, CrossFitTraining,
    FlexibilityTraining, MuscleGroup, PersonalDietPlan, PersonalWorkoutPlan,
    Profile, Recovery, ResistanceTraining, TrainingLevel, UserFoodLog,
)

# Serializer for Profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        extra_kwargs = {"user": {"read_only": True}}


# Serializer for User details
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "profile",
        ]
        extra_kwargs = {
            "password": {"write_only": True},  # Make password write-only
        }

    def create(self, validated_data):
        profile_data = validated_data.pop("profile", None)
        password = validated_data.pop("password")
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        if profile_data:
            Profile.objects.create(user=user, **profile_data)
        return user


# Serializer for certain Muscle Group
class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = ["id", "name"]


# Serializer for Training level
class TrainingLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainingLevel
        fields = ["id", "current_level"]


# Serializers for Workouts and Physical activities
class ResistanceTrainingSerializer(serializers.ModelSerializer):
    muscle_group = MuscleGroupSerializer()
    current_level = TrainingLevelSerializer()

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
    current_level = TrainingLevelSerializer()

    class Meta:
        model = CardioTraining
        fields = ["id", "exercise_name", "duration", "intensity", "current_level"]


# Serializer for cardio
class CrossFitTrainingSerializer(serializers.ModelSerializer):
    current_level = TrainingLevelSerializer()

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


# Serializer for updating body metrics
class BodyMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BodyMetrics
        fields = ["weight", "date", "profile"]
        read_only_fields = ["profile"]


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


# Serializer for personal workout plan with ManyToMany relations
class PersonalWorkoutPlanSerializer(serializers.ModelSerializer):
    resistance_trainings = ResistanceTrainingSerializer(many=True, read_only=True)
    cardio_trainings = CardioTrainingSerializer(many=True, read_only=True)
    crossfit_trainings = CrossFitTrainingSerializer(many=True, read_only=True)
    flexibility_trainings = FlexibilityTrainingSerializer(many=True, read_only=True)
    recoveries = RecoverySerializer(many=True, read_only=True)

    # Adding extra `write_only` fields for accepting input IDs during creation
    resistance_trainings_ids = serializers.PrimaryKeyRelatedField(
        queryset=ResistanceTraining.objects.all(), many=True, write_only=True
    )
    cardio_trainings_ids = serializers.PrimaryKeyRelatedField(
        queryset=CardioTraining.objects.all(), many=True, write_only=True
    )
    crossfit_trainings_ids = serializers.PrimaryKeyRelatedField(
        queryset=CrossFitTraining.objects.all(), many=True, write_only=True
    )
    flexibility_trainings_ids = serializers.PrimaryKeyRelatedField(
        queryset=FlexibilityTraining.objects.all(), many=True, write_only=True
    )
    recoveries_ids = serializers.PrimaryKeyRelatedField(
        queryset=Recovery.objects.all(), many=True, write_only=True
    )

    class Meta:
        model = PersonalWorkoutPlan
        fields = [
            "profile",
            "start_date",
            "end_date",
            "resistance_trainings",
            "cardio_trainings",
            "crossfit_trainings",
            "flexibility_trainings",
            "recoveries",
            # Fields for writing IDs
            "resistance_trainings_ids",
            "cardio_trainings_ids",
            "crossfit_trainings_ids",
            "flexibility_trainings_ids",
            "recoveries_ids",
        ]

    def create(self, validated_data):
        # Extract the IDs for ManyToMany relationships
        resistance_ids = validated_data.pop("resistance_trainings_ids", [])
        cardio_ids = validated_data.pop("cardio_trainings_ids", [])
        crossfit_ids = validated_data.pop("crossfit_trainings_ids", [])
        flexibility_ids = validated_data.pop("flexibility_trainings_ids", [])
        recovery_ids = validated_data.pop("recoveries_ids", [])

        # Create the PersonalWorkoutPlan instance
        workout_plan = PersonalWorkoutPlan.objects.create(**validated_data)

        # Assign the ManyToMany relationships
        workout_plan.resistance_trainings.set(resistance_ids)
        workout_plan.cardio_trainings.set(cardio_ids)
        workout_plan.crossfit_trainings.set(crossfit_ids)
        workout_plan.flexibility_trainings.set(flexibility_ids)
        workout_plan.recoveries.set(recovery_ids)

        return workout_plan


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
