from django.test import SimpleTestCase
from django.urls import reverse, resolve
from myfitapp.views import (
    CardioTrainingView,
    CrossFitTrainingView,
    FlexibilityTrainingView,
    ListFoodsView,
    PersonalDietPlanView,
    PersonalWorkoutPlanView,
    RecoveryView,
    ResistanceTrainingView,
    SearchFoodView,
    SearchRecipe,
    UserFoodLogView,
)


class TestUrls(SimpleTestCase):

    def test_food_log_url_is_resolves(self):
        url = reverse("food_log")
        self.assertEqual(resolve(url).func.view_class, UserFoodLogView)

    def test_list_foods_url_is_resolves(self):
        url = reverse("list_foods")
        self.assertEqual(resolve(url).func.view_class, ListFoodsView)

    def test_nutrition_url_is_resolves(self):
        url = reverse("nutrition")
        self.assertEqual(resolve(url).func.view_class, SearchFoodView)

    def test_recipe_url_is_resolves(self):
        url = reverse("recipe")
        self.assertEqual(resolve(url).func.view_class, SearchRecipe)

    def test_resistance_url_is_resolves(self):
        url = reverse("resistance")
        self.assertEqual(resolve(url).func.view_class, ResistanceTrainingView)

    def test_cardio_url_is_resolves(self):
        url = reverse("cardio")
        self.assertEqual(resolve(url).func.view_class, CardioTrainingView)

    def test_crossfit_url_is_resolves(self):
        url = reverse("crossfit")
        self.assertEqual(resolve(url).func.view_class, CrossFitTrainingView)

    def test_flexibility_url_is_resolves(self):
        url = reverse("flexibility")
        self.assertEqual(resolve(url).func.view_class, FlexibilityTrainingView)

    def test_recovery_url_is_resolves(self):
        url = reverse("recovery")
        self.assertEqual(resolve(url).func.view_class, RecoveryView)

    def test_workout_plan_url_is_resolves(self):
        url = reverse("workout_plan")
        self.assertEqual(resolve(url).func.view_class, PersonalWorkoutPlanView)

    def test_diet_plan_url_is_resolves(self):
        url = reverse("diet_plan")
        self.assertEqual(resolve(url).func.view_class, PersonalDietPlanView)
