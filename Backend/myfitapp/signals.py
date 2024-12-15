from django.db.models.signals import post_save
from django.dispatch import receiver
from myfitapp.models import PersonalDietPlan
from authentication.models import Profile
from django.utils import timezone
import logging
from myfitapp.scripts import calculate_end_date

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Profile)
def create_or_update_diet_plan(sender, instance, created, **kwargs):
    """
    Signal to create or update a personal diet plan whenever
    the profile is updated.
    """
    logger.info(f"Signal Triggered for Profile: {instance.id}")

    # Check if profile has valid weight and goal
    if instance.weight and instance.weight > 0 and instance.goal:
        plan, created = PersonalDietPlan.objects.get_or_create(profile=instance)
        
        if not created:
            # Update existing plan with new data
            plan.calorie_budget = plan.calculate_calorie_budget()
            plan.protein, plan.carbs, plan.fats = plan.calculate_macros()
            plan.start_date = timezone.now().date()
            plan.end_date = calculate_end_date(plan.start_date)
            plan.save()
        logger.info("Diet Plan Created/Updated Successfully")
    else:
        logger.warning(f"Profile {instance.id} does not have a valid weight or goal")