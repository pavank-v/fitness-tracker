from django.utils import timezone

from myfitapp.models import UserFoodLog, PersonalDietPlan


# this method will give a detailed summary about the food consumption
# on the day "Tracking Calories"
def daily_summary(profile):

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
