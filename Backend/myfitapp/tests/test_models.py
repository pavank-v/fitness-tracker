from django.test import TestCase
from django.contrib.auth.models import User
from unittest.mock import patch

from myfitapp.choices import GenderChoices, GoalChoices
from myfitapp.models import (
    ResistanceTraining,
    MuscleGroup,
    CardioTraining,
    CrossFitTraining,
    FlexibilityTraining,
    Recovery,
    PersonalWorkoutPlan,
    PersonalDietPlan,
    UserFoodLog,
)
from authentication.models import Profile


class TestResistanceTraining(TestCase):

    def setUp(self):
        self.muscle_group = MuscleGroup.objects.create(name="legs")
        self.resistance = ResistanceTraining.objects.create(
            exercise_name="Squats",
            sets="3 to 4",
            reps="6 to 8",
            muscle_group=self.muscle_group,
            current_level="Beginner",
        )

    def test_resistance_training_is_assigned(self):
        self.assertEqual(self.resistance.exercise_name, "Squats")
        self.assertEqual(self.resistance.sets, "3 to 4")
        self.assertEqual(self.resistance.reps, "6 to 8")
        self.assertEqual(self.resistance.muscle_group, self.muscle_group)
        self.assertEqual(self.resistance.current_level, "Beginner")


class TestCardioTraining(TestCase):

    def setUp(self):
        self.cardio = CardioTraining.objects.create(
            exercise_name="Running",
            duration=60,
            intensity="Low",
            current_level="Beginner",
        )

    def test_cardio_training_is_assigned(self):
        self.assertEqual(self.cardio.exercise_name, "Running")
        self.assertEqual(self.cardio.duration, 60)
        self.assertEqual(self.cardio.intensity, "Low")
        self.assertEqual(self.cardio.current_level, "Beginner")


class TestCrossFitTraining(TestCase):

    def setUp(self):
        self.crossfit = CrossFitTraining.objects.create(
            exercise_name="double unders",
            rounds=5,
            time_cap=2,
            current_level="Intermediate",
        )

    def test_crossfit_training_is_assigned(self):
        self.assertEqual(self.crossfit.exercise_name, "double unders")
        self.assertEqual(self.crossfit.rounds, 5)
        self.assertEqual(self.crossfit.time_cap, 2)
        self.assertEqual(self.crossfit.current_level, "Intermediate")


class TestFlexibilityTraining(TestCase):

    def setUp(self):
        self.flexiblity = FlexibilityTraining.objects.create(
            exercise_name="pike pose",
            duration=30,
            stretch_type="Static",
            current_level="Intermediate",
        )

    def test_flexiblity_training_is_assigned(self):
        self.assertEqual(self.flexiblity.exercise_name, "pike pose")
        self.assertEqual(self.flexiblity.duration, 30)
        self.assertEqual(self.flexiblity.stretch_type, "Static")
        self.assertEqual(self.flexiblity.current_level, "Intermediate")


class TestRecovery(TestCase):

    def setUp(self):
        self.recovery = Recovery.objects.create(
            method_name="cold plunge",
            duration=30,
            recovery_type="Active",
            current_level="Intermediate",
        )

    def test_recovery_training_is_assigned(self):
        self.assertEqual(self.recovery.method_name, "cold plunge")
        self.assertEqual(self.recovery.duration, 30)
        self.assertEqual(self.recovery.recovery_type, "Active")
        self.assertEqual(self.recovery.current_level, "Intermediate")


class TestPersonalWorkoutPlan(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", password="password")
        self.profile = Profile.objects.create(
            user=self.user,
            age=20,
            gender="M",
            height=180.0,
            weight=75.4,
            current_level="Beginner",
            body_fat_percentage=17,
            goal="Lose",
        )
        self.muscle_group = MuscleGroup.objects.create(name="legs")
        self.resistance = ResistanceTraining.objects.create(
            exercise_name="Squats",
            sets="3 to 4",
            reps="6 to 8",
            muscle_group=self.muscle_group,
            current_level="Beginner",
        )
        self.cardio = CardioTraining.objects.create(
            exercise_name="Running",
            duration=60,
            intensity="Low",
            current_level="Beginner",
        )
        self.crossfit = CrossFitTraining.objects.create(
            exercise_name="double unders",
            rounds=5,
            time_cap=2,
            current_level="Intermediate",
        )
        self.flexiblity = FlexibilityTraining.objects.create(
            exercise_name="pike pose",
            duration=30,
            stretch_type="Static",
            current_level="Intermediate",
        )
        self.recovery = Recovery.objects.create(
            method_name="cold plunge",
            duration=30,
            recovery_type="Active",
            current_level="Intermediate",
        )
        self.workout_plan = PersonalWorkoutPlan.objects.create(profile=self.profile)
        self.workout_plan.resistance_trainings.add(self.resistance)
        self.workout_plan.cardio_trainings.add(self.cardio)
        self.workout_plan.crossfit_trainings.add(self.crossfit)
        self.workout_plan.flexibility_trainings.add(self.flexiblity)
        self.workout_plan.recoveries.add(self.recovery)

    def test_workout_plan_creation(self):
        self.assertEqual(self.workout_plan.profile, self.profile)

    def test_workouts_in_workout_plan(self):
        self.assertIn(self.resistance, self.workout_plan.resistance_trainings.all())
        self.assertIn(self.cardio, self.workout_plan.cardio_trainings.all())
        self.assertIn(self.crossfit, self.workout_plan.crossfit_trainings.all())
        self.assertIn(self.flexiblity, self.workout_plan.flexibility_trainings.all())
        self.assertIn(self.recovery, self.workout_plan.recoveries.all())

    def test_start_date_auto_populated(self):
        self.assertIsNotNone(self.workout_plan.start_date)

    def test_end_date_can_be_blank_or_null(self):
        self.assertIsNone(self.workout_plan.end_date)

    def test_workout_plan_str(self):
        expected_str = f"{self.profile.user.username} - Workout Plan"
        self.assertEqual(str(self.workout_plan), expected_str)


class TestPersonalDietPlan(TestCase):

    def setUp(self):
        self.male_user = User.objects.create(username="male_user", password="password")
        self.male_profile = Profile.objects.create(
            user=self.male_user,
            weight=70.7,
            gender=GenderChoices.MALE,
            goal=GoalChoices.MAINTAIN,
        )
        self.female_user = User.objects.create(
            username="female_user", password="password"
        )
        self.female_profile = Profile.objects.create(
            user=self.female_user,
            weight=60.5,
            gender=GenderChoices.FEMALE,
            goal=GoalChoices.LOSE,
        )

    def test_diet_plan_created_on_profile_creation(self):
        male_diet_plan = PersonalDietPlan.objects.filter(
            profile=self.male_profile
        ).first()
        female_diet_plan = PersonalDietPlan.objects.filter(
            profile=self.female_profile
        ).first()

        self.assertIsNotNone(male_diet_plan)
        self.assertIsNotNone(female_diet_plan)

    def test_macros_calculated_on_diet_plan_creation(self):
        male_diet_plan = PersonalDietPlan.objects.get(profile=self.male_profile)
        female_diet_plan = PersonalDietPlan.objects.get(profile=self.female_profile)

        expected_male_protein = round(male_diet_plan.calorie_budget * 0.3) // 4
        expected_male_carbs = round(male_diet_plan.calorie_budget * 0.5) // 4
        expected_male_fats = round(male_diet_plan.calorie_budget * 0.2) // 9

        total_calores = (
            (expected_male_carbs * 4)
            + (expected_male_protein * 4)
            + (expected_male_fats * 9)
        )
        adjustment = (male_diet_plan.calorie_budget - total_calores) // 4
        expected_male_carbs += adjustment

        self.assertEqual(
            (male_diet_plan.protein, male_diet_plan.carbs, male_diet_plan.fats),
            (expected_male_protein, expected_male_carbs, expected_male_fats),
        )

        expected_female_protein = round(female_diet_plan.calorie_budget * 0.25) // 4
        expected_female_carbs = round(female_diet_plan.calorie_budget * 0.4) // 4
        expected_female_fats = round(female_diet_plan.calorie_budget * 0.35) // 9

        total_calores = (
            (expected_female_carbs * 4)
            + (expected_female_protein * 4)
            + (expected_female_fats * 9)
        )
        adjustment = (female_diet_plan.calorie_budget - total_calores) // 4
        expected_female_carbs += adjustment
        self.assertEqual(
            (female_diet_plan.protein, female_diet_plan.carbs, female_diet_plan.fats),
            (expected_female_protein, expected_female_carbs, expected_female_fats),
        )

    def test_diet_plan_updated_on_profile_update(self):
        self.male_profile.weight = 75
        self.male_profile.goal = GoalChoices.GAIN
        self.male_profile.save()

        updated_male_diet_plan = PersonalDietPlan.objects.get(profile=self.male_profile)
        expected_updated_budget = round(75 * 2.202 * 16)
        self.assertAlmostEqual(
            updated_male_diet_plan.calorie_budget, expected_updated_budget
        )

        expected_updated_protein = round(expected_updated_budget * 0.3) // 4
        expected_updated_carbs = round(expected_updated_budget * 0.5) // 4
        expected_updated_fats = round(expected_updated_budget * 0.2) // 9

        total_calores = (
            (expected_updated_protein * 4)
            + (expected_updated_carbs * 4)
            + (expected_updated_fats * 9)
        )
        adjustment = (updated_male_diet_plan.calorie_budget - total_calores) // 4
        expected_updated_carbs += adjustment

        self.assertEqual(
            (
                updated_male_diet_plan.protein,
                updated_male_diet_plan.carbs,
                updated_male_diet_plan.fats,
            ),
            (expected_updated_protein, expected_updated_carbs, expected_updated_fats),
        )

    def test_diet_plan_created_with_zero_weight(self):
        self.zero_user = User.objects.create(username="zero_user", password="password")
        zero_weight_profile = Profile.objects.create(
            user=self.zero_user,
            weight=0,
            gender=GenderChoices.MALE,
            goal=GoalChoices.LOSE,
        )

        diet_plan_exists = PersonalDietPlan.objects.filter(
            profile=zero_weight_profile
        ).exists()
        self.assertFalse(
            diet_plan_exists,
            "Diet plan should not be created for profile with zero weight",
        )


class TestUserFoodLog(TestCase):

    def setUp(self):

        self.user = User.objects.create(username="testuser", password="password")
        self.profile = Profile.objects.create(
            user=self.user, weight=70, gender="M", goal="Maintain"
        )

    @patch("myfitapp.models.calories_finder")
    def test_create_food_log(self, mock_calories_finder):
        mock_calories_finder.return_value = {
            "calories": 250.00,
            "protein_g": 15.00,
            "carbohydrates_total_g": 30.00,
            "fat_total_g": 10.00,
        }

        food_log = UserFoodLog.objects.create(
            profile=self.profile, food_name="Apple", quantity=150
        )

        self.assertEqual(food_log.calories, 250.00)
        self.assertEqual(food_log.protein_intake, 15.00)
        self.assertEqual(food_log.carbs_intake, 30.00)
        self.assertEqual(food_log.fat_intake, 10.00)
        self.assertEqual(food_log.profile, self.profile)

    @patch("myfitapp.models.calories_finder")
    def test_food_log_with_missing_nutrition(self, mock_calories_finder):
        mock_calories_finder.return_value = {
            "calories": None,
            "protein_g": None,
            "carbohydrates_total_g": None,
            "fat_total_g": None,
        }

        food_log = UserFoodLog.objects.create(
            profile=self.profile, food_name="Mystery Food", quantity=100
        )

        self.assertIsNone(food_log.calories)
        self.assertIsNone(food_log.protein_intake)
        self.assertIsNone(food_log.carbs_intake)
        self.assertIsNone(food_log.fat_intake)

    def test_user_food_log_str(self):
        food_log = UserFoodLog.objects.create(
            profile=self.profile, food_name="Banana", quantity=200
        )
        self.assertEqual(str(food_log), "Banana - 200g")
