from django.urls import path

from myfitapp.views import (CardioTrainingView, SearchRecipe,
    CrossFitTrainingView, FlexibilityTrainingView, UserFoodLogView,
    ListFoodsView, PersonalDietPlanView, PersonalWorkoutPlanView,
    RecoveryView, ResistanceTrainingView, SearchFoodView,

)

urlpatterns = [
    # Endpoints for Food Logging and listing
    path("food-log/", UserFoodLogView.as_view(), name="food_log"),
    path("list-foods/", ListFoodsView.as_view(), name="list_foods"),

    # Endpoints for searching foods and recipes
    path("search-nutritional-facts/", SearchFoodView.as_view(), name="nutrition"),
    path("recipe/", SearchRecipe.as_view(), name="recipe"),

    # Endpoints for workouts
    path("resistance-training/", ResistanceTrainingView.as_view(), name="resistance"),
    path("cardio-training/", CardioTrainingView.as_view(), name="cardio"),
    path("crossfit-training/", CrossFitTrainingView.as_view(), name="crossfit"),
    path(
        "flexibility-training/", FlexibilityTrainingView.as_view(), name="flexibility"
    ),
    path("recovery/", RecoveryView.as_view(), name="recovery"),

    # Endpoints for Personalized workout and diet plan
    path(
        "personal-workout-plan/", PersonalWorkoutPlanView.as_view(), name="workout_plan"
    ), 
    path("personal-diet-plan/", PersonalDietPlanView.as_view(), name="diet_plan"),
]
