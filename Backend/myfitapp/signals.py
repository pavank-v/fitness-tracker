from django.db.models.signals import post_save
from django.dispatch import receiver
from myfitapp.models import PersonalDietPlan, Profile
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Profile)
def create_or_update_diet_plan(sender, instance, created, **kwargs):
    """
    signal to create a personal diet plan automatically whenever
    the profile is updated
    """
    logger.info(f"Signal Triggered for Profile: {instance.id}")

    if instance.weight:
        PersonalDietPlan.objects.get_or_create(profile=instance)
        logger.info("Diet Plan Created Successfully")
    else:
        logger.warning("Profile Does not have Weight and Goal")


