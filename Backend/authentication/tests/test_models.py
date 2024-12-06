from django.test import TestCase
from django.contrib.auth.models import User
from authentication.models import Profile
from myfitapp.choices import GenderChoices, LevelChoices, GoalChoices


class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="password123", email="testuser@example.com"
        )
        self.profile = Profile.objects.create(
            user=self.user,
            age=25,
            gender=GenderChoices.MALE,
            weight=70.5,
            height=175.0,
            current_level=LevelChoices.INTERMEDIATE,
            body_fat_percentage=15.5,
            goal=GoalChoices.MAINTAIN,
        )

    def test_profile_creation(self):
        self.assertEqual(self.profile.user.username, "testuser")
        self.assertEqual(self.profile.age, 25)
        self.assertEqual(self.profile.gender, GenderChoices.MALE)
        self.assertEqual(self.profile.weight, 70.5)
        self.assertEqual(self.profile.height, 175.0)
        self.assertEqual(self.profile.current_level, LevelChoices.INTERMEDIATE)
        self.assertEqual(self.profile.body_fat_percentage, 15.5)
        self.assertEqual(self.profile.goal, GoalChoices.MAINTAIN)

    def test_profile_str_representation(self):
        self.assertEqual(str(self.profile), "testuser")

    def test_profile_update(self):
        self.profile.age = 30
        self.profile.weight = 75.0
        self.profile.save()

        updated_profile = Profile.objects.get(user=self.user)
        self.assertEqual(updated_profile.age, 30)
        self.assertEqual(updated_profile.weight, 75.0)

    def test_default_values(self):
        new_user = User.objects.create_user(username="defaultuser", password="password")
        new_profile = Profile.objects.create(user=new_user, weight=65.0)
        self.assertEqual(new_profile.gender, GenderChoices.MALE)
        self.assertEqual(new_profile.current_level, LevelChoices.BEGINNER)
        self.assertEqual(new_profile.goal, GoalChoices.MAINTAIN)
        self.assertIsNone(new_profile.height)
        self.assertIsNone(new_profile.body_fat_percentage)
