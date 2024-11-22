from django.urls import path

from .views import (
    BodyMetricsUpdateView,
    CardioTrainingView,
    CrossFitTrainingView,
    FlexibilityTrainingView,
    FoodLogCreateView,
    ListFoodsView,
    RecoveryView,
    ResistanceTrainingView,
    SearchFoodView,
    SearchRecipe,
)

urlpatterns = [
    path("update/", BodyMetricsUpdateView.as_view(), name="update"),
    path("food-log/", FoodLogCreateView.as_view(), name="food-log"),
    path("list_foods/", ListFoodsView.as_view(), name="list_foods"),
    path("search-nutritional-facts/", SearchFoodView.as_view(), name="nutrition"),
    path("recipe/", SearchRecipe.as_view(), name="recipe"),
    path("resistance-training/", ResistanceTrainingView.as_view(), name="resistance"),
    path("cardio-training/", CardioTrainingView.as_view(), name="cardio"),
    path("crossfit-training/", CrossFitTrainingView.as_view(), name="crossfit"),
    path(
        "flexibility-training/", FlexibilityTrainingView.as_view(), name="flexibility"
    ),
    path("recovery/", RecoveryView.as_view(), name="recovery"),
]
