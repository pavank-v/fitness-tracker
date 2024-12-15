from rest_framework.test import APITestCase, APIRequestFactory
from django.contrib.auth.models import User
from myfitapp.models import (
    MuscleGroup,
    CardioTraining,
    CrossFitTraining,
    FlexibilityTraining,
    ResistanceTraining,
)
from myfitapp.serializers import (
    MuscleGroupSerializer,
    CardioTrainingSerializer,
    CrossFitTrainingSerializer,
    FlexibilityTrainingSerializer,
    PersonalDietPlanSerializer,
    PersonalWorkoutPlanSerializer,
    RecipeSerializer,
    ResistanceTrainingSerializer,
    SearchSerializer,
)
from authentication.models import Profile


class MuscleGroupSerializerTest(APITestCase):
    def setUp(self):
        self.muscle_group = MuscleGroup.objects.create(name="Chest")

    def test_muscle_group_serializer(self):
        serializer = MuscleGroupSerializer(instance=self.muscle_group)
        self.assertEqual(serializer.data["name"], "Chest")

    def test_create_muscle_group(self):
        data = {"name": "Back"}
        serializer = MuscleGroupSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        muscle_group = serializer.save()
        self.assertEqual(muscle_group.name, "Back")


class ResistanceTrainingSerializerTest(APITestCase):
    def setUp(self):
        self.muscle_group = MuscleGroup.objects.create(name="Chest")
        self.resistance_training = ResistanceTraining.objects.create(
            exercise_name="Push Up",
            sets="3",
            reps="15",
            muscle_group=self.muscle_group,
            current_level="Beginner",
        )

    def test_resistance_training_serializer(self):
        serializer = ResistanceTrainingSerializer(instance=self.resistance_training)
        self.assertEqual(serializer.data["exercise_name"], "Push Up")
        self.assertEqual(serializer.data["sets"], "3")
        self.assertEqual(serializer.data["reps"], "15")


class CardioTrainingSerializerTest(APITestCase):
    def setUp(self):
        self.cardio_training = CardioTraining.objects.create(
            exercise_name="Running",
            duration=30,
            intensity="Medium",
            current_level="Beginner",
        )

    def test_cardio_training_serializer(self):
        serializer = CardioTrainingSerializer(instance=self.cardio_training)
        self.assertEqual(serializer.data["exercise_name"], "Running")
        self.assertEqual(serializer.data["duration"], 30)

    def test_create_cardio_training(self):
        data = {
            "exercise_name": "Cycling",
            "duration": 45,
            "intensity": "High",
            "current_level": "Intermediate",
        }
        serializer = CardioTrainingSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        cardio_training = serializer.save()
        self.assertEqual(cardio_training.exercise_name, "Cycling")


class CrossFitTrainingSerializerTest(APITestCase):
    def setUp(self):
        self.crossfit_training = CrossFitTraining.objects.create(
            exercise_name="Burpees", rounds=5, time_cap=10, current_level="Beginner"
        )

    def test_crossfit_training_serializer(self):
        serializer = CrossFitTrainingSerializer(instance=self.crossfit_training)
        self.assertEqual(serializer.data["exercise_name"], "Burpees")
        self.assertEqual(serializer.data["rounds"], 5)


class FlexibilityTrainingSerializerTest(APITestCase):
    def setUp(self):
        self.flexibility_training = FlexibilityTraining.objects.create(
            exercise_name="Yoga", duration=30, current_level="Beginner"
        )

    def test_flexibility_training_serializer(self):
        serializer = FlexibilityTrainingSerializer(instance=self.flexibility_training)
        self.assertEqual(serializer.data["exercise_name"], "Yoga")
        self.assertEqual(serializer.data["duration"], 30)


class PersonalWorkoutPlanSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.profile = Profile.objects.create(user=self.user, weight=68.0, height=170.9)
        self.client.login(username="testuser", password="testpass")

        self.muscle_group = MuscleGroup.objects.create(name="Chest")
        self.resistance_training = ResistanceTraining.objects.create(
            exercise_name="Push Up",
            sets=3,
            reps=15,
            muscle_group=self.muscle_group,
            current_level="Beginner",
        )

        self.factory = APIRequestFactory()
        self.request = self.factory.post("/fake-url")
        self.request.user = self.user

    def test_create_personal_workout_plan(self):
        data = {
            "profile": self.profile.id,
            "start_date": "2024-12-01",
            "end_date": "2024-12-31",
            "level": "Beginner",
            "workout_type": "Resistance",
        }
        serializer = PersonalWorkoutPlanSerializer(
            data=data, context={"request": self.request}
        )
        self.assertTrue(serializer.is_valid())
        workout_plan = serializer.save()
        self.assertEqual(workout_plan.resistance_trainings.count(), 1)


class PersonalDietPlanSerializerTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.profile = Profile.objects.create(user=self.user, weight=68.0, height=170.9)
        self.client.login(username="testuser", password="testpass")

    def test_create_personal_diet_plan(self):
        data = {
            "profile": self.profile.id,
            "start_date": "2024-12-01",
            "end_date": "2024-12-31",
        }
        serializer = PersonalDietPlanSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        diet_plan = serializer.save()
        self.assertEqual(diet_plan.profile, self.user.profile)


class SearchSerializerTest(APITestCase):
    def test_search_serializer(self):
        data = {"food_name": "Apple", "quantity": 100}
        serializer = SearchSerializer(data=data)
        self.assertTrue(serializer.is_valid())


class RecipeSerializerTest(APITestCase):
    def test_recipe_serializer(self):
        data = {"food_name": "Apple"}
        serializer = RecipeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
