from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from authentication.models import Profile
from myfitapp.models import (
    UserFoodLog,
    MuscleGroup,
    PersonalDietPlan,
    ResistanceTraining,
    CardioTraining,
    CrossFitTraining,
    FlexibilityTraining,
    Recovery,
    PersonalWorkoutPlan,
    PersonalDietPlan,
)
from datetime import date
from myfitapp.choices import LevelChoices


class TestSearchFoodView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.profile = Profile.objects.create(user=self.user, weight=70, height=175)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("nutrition")

    def test_search_food_valid(self):
        data = {"food_name": "apple", "quantity": 100}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("calories", response.data)

    def test_search_food_invalid_food_name(self):
        data = {"food_name": "", "quantity": 100}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_search_food_missing_quantity(self):
        data = {"food_name": "apple"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn("quantity", response.data)


class TestSearchRecipeView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.profile = Profile.objects.create(user=self.user, weight=70, height=175)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("recipe")

    def test_search_recipe_valid(self):
        data = {"food_name": "Pasta"}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data)

    def test_search_recipe_invalid_food_name(self):
        data = {"food_name": ""}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestListFoodsView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.profile = Profile.objects.create(user=self.user, weight=70, height=175)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("list_foods")

        self.food_log_today = UserFoodLog.objects.create(
            profile=self.profile,
            food_name="Apple",
            quantity=150,
            calories=72,
            date=date.today(),
        )
        self.food_log_other_day = UserFoodLog.objects.create(
            profile=self.profile,
            food_name="Banana",
            quantity=120,
            calories=89,
            date=date(2024, 12, 1),
        )

    def test_list_foods_for_today(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["food_name"], "Apple")

    def test_list_foods_with_invalid_date_format(self):
        response = self.client.get(self.url, {"date": "12-01-2024"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid date format", response.data["error"])


class TestUserFoodLogView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.profile = Profile.objects.create(user=self.user, weight=70, height=175)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("food_log")

        self.food_log = UserFoodLog.objects.create(
            profile=self.profile,
            food_name="Apple",
            quantity=150,
            calories=72,
            date=date.today(),
        )

    def test_post_food_log(self):
        data = {
            "food_name": "Banana",
            "quantity": 120,
            "calories": 89,
            "date": str(date.today()),
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("food-log", response.data)
        self.assertEqual(response.data["food-log"]["food_name"], "Banana")

    def test_get_food_logs(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("daily_summary", response.data)
        self.assertEqual(len(response.data["food-log"]), 1)
        self.assertEqual(response.data["food-log"][0]["food_name"], "Apple")

    def test_delete_food_log(self):
        data = {
            "food_name": "Apple",
            "date": str(date.today()),
        }
        response = self.client.delete(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("detail", response.data)
        self.assertEqual(response.data["detail"], "Apple - deleted successfully.")


class TestPersonalDietPlanView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.profile = Profile.objects.create(user=self.user, weight=70, height=175)
        self.client.force_authenticate(user=self.user)
        self.url = reverse("diet_plan")

        self.diet_plan1 = PersonalDietPlan.objects.create(
            profile=self.profile, calorie_budget=2100, protein=200, carbs=100, fats=100
        )

    def test_get_personal_diet_plan_success(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_personal_diet_plan_no_profile(self):
        self.profile.delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Profile not found for the user.")


class TestResistanceTrainingView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.muscle_group = MuscleGroup.objects.create(name="Chest")
        self.exercise1 = ResistanceTraining.objects.create(
            exercise_name="Bench Press",
            muscle_group=self.muscle_group,
            current_level=LevelChoices.BEGINNER,
        )
        self.exercise2 = ResistanceTraining.objects.create(
            exercise_name="Push Ups",
            muscle_group=self.muscle_group,
            current_level=LevelChoices.INTERMEDIATE,
        )
        self.url = reverse("resistance")

    def test_get_resistance_training(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(len(response.data["results"]))

    def test_get_resistance_training_filter_by_muscle_group(self):
        response = self.client.get(self.url, {"muscle_group": "Chest"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(len(response.data["results"]))

    def test_get_resistance_training_filter_by_training_level(self):
        response = self.client.get(self.url, {"current_level": "Beginner"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(len(response.data["results"]))


class TestCardioTrainingView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.exercise1 = CardioTraining.objects.create(
            exercise_name="Running",
            current_level=LevelChoices.BEGINNER,
            duration=30,
            intensity="Low",
        )
        self.exercise2 = CardioTraining.objects.create(
            exercise_name="Cycling",
            current_level=LevelChoices.INTERMEDIATE,
            duration=30,
            intensity="Low",
        )
        self.url = reverse("cardio")

    def test_get_cardio_training(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_get_cardio_training_filter_by_training_level(self):
        response = self.client.get(self.url, {"current_level": "Intermediate"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)


class TestCrossFitTrainingView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.exercise1 = CrossFitTraining.objects.create(
            exercise_name="Burpees",
            current_level=LevelChoices.BEGINNER,
            rounds=5,
            time_cap=30,
        )
        self.exercise2 = CrossFitTraining.objects.create(
            exercise_name="Deadlift",
            current_level=LevelChoices.BEGINNER,
            rounds=5,
            time_cap=30,
        )
        self.url = reverse("crossfit")

    def test_get_crossfit_training(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_get_crossfit_training_filter_by_training_level(self):
        response = self.client.get(self.url, {"current_level": "Advanced"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)


class TestFlexibilityTrainingView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.stretch1 = FlexibilityTraining.objects.create(
            exercise_name="Hamstring Stretch",
            duration=30,
            stretch_type="Static",
            current_level=LevelChoices.BEGINNER,
        )
        self.stretch2 = FlexibilityTraining.objects.create(
            exercise_name="Quad Stretch",
            duration=30,
            stretch_type="Static",
            current_level=LevelChoices.BEGINNER,
        )
        self.url = reverse("flexibility")

    def test_get_flexibility_training(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)


class TestRecoveryView(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.client.force_authenticate(user=self.user)
        self.method1 = Recovery.objects.create(
            method_name="Foam Rolling",
            duration=30,
            recovery_type="Active",
            current_level=LevelChoices.BEGINNER,
        )
        self.method2 = Recovery.objects.create(
            method_name="Ice Bath",
            duration=30,
            recovery_type="Active",
            current_level=LevelChoices.BEGINNER,
        )
        self.url = reverse("recovery")

    def test_get_recovery_methods(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)


class TestPersonalWorkoutPlanView(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", password="password123"
        )
        self.profile = Profile.objects.create(user=self.user, weight=70, height=175)
        self.client.force_authenticate(user=self.user)
        self.muscle_group = MuscleGroup.objects.create(name="Chest")
        self.exercise1 = ResistanceTraining.objects.create(
            exercise_name="Bench Press",
            muscle_group=self.muscle_group,
            current_level=LevelChoices.BEGINNER,
        )
        self.exercise2 = ResistanceTraining.objects.create(
            exercise_name="Push Ups",
            muscle_group=self.muscle_group,
            current_level=LevelChoices.INTERMEDIATE,
        )
        self.url = reverse("workout_plan")

    def test_create_personal_workout_plan(self):
        data = {
            "level": "Beginner",
            "workout_type": "Resistance",
            "start_date": "2024-12-06",
            "end_date": "2024-12-20",
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Workout plan created successfully.")
        workout_plan = PersonalWorkoutPlan.objects.get(profile=self.user.profile)
        self.assertIsNotNone(workout_plan)

    def test_create_personal_workout_plan_duplicate(self):
        data = {
            "level": "Beginner",
            "workout_type": "Resistance",
            "start_date": "2024-12-06",
            "end_date": "2024-12-20",
        }
        self.client.post(self.url, data)

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "A Resistance workout plan for level 'Beginner' already exists.",
            response.data["message"],
        )

    def test_get_personal_workout_plan(self):
        data = {
            "level": "Beginner",
            "workout_type": "Resistance",
            "start_date": "2024-12-06",
            "end_date": "2024-12-20",
        }
        self.client.post(self.url, data)

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_personal_workout_plan_no_plans(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["message"], "No workout plans found.")

    def test_get_personal_workout_plan_filter_by_type(self):
        data = {
            "level": "Beginner",
            "workout_type": "Resistance",
            "start_date": "2024-12-06",
            "end_date": "2024-12-20",
        }
        self.client.post(self.url, data)

        response = self.client.get(self.url, {"workout_type": "Resistance"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_get_personal_workout_plan_filter_by_level(self):
        data = {
            "level": "Beginner",
            "workout_type": "Resistance",
            "start_date": "2024-12-06",
            "end_date": "2024-12-20",
        }
        self.client.post(self.url, data)

        response = self.client.get(self.url, {"level": "Beginner"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_delete_personal_workout_plan(self):
        data = {
            "level": "Beginner",
            "workout_type": "Resistance",
            "start_date": "2024-12-06",
            "end_date": "2024-12-20",
        }
        self.client.post(self.url, data)

        delete_data = {"level": "Beginner", "workout_type": "Resistance"}
        response = self.client.delete(self.url, delete_data)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            response.data["detail"], "Resistance workout plan deleted successfully."
        )

    def test_delete_personal_workout_plan_not_found(self):
        delete_data = {"level": "Intermediate", "workout_type": "Cardio"}
        response = self.client.delete(self.url, delete_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response.data["detail"],
            "No Cardio workout plans found for level Intermediate.",
        )

    def test_delete_personal_workout_plan_invalid_type(self):
        delete_data = {"level": "Beginner", "workout_type": "InvalidType"}
        response = self.client.delete(self.url, delete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid workout type.")

    def test_delete_personal_workout_plan_invalid_level(self):
        delete_data = {"level": "InvalidLevel", "workout_type": "Resistance"}
        response = self.client.delete(self.url, delete_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Invalid level.")
