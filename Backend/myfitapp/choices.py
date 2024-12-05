from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

class LevelChoices(TextChoices):
    BEGINNER = 'Beginner', _('Beginner')
    INTERMEDIATE = 'Intermediate', _('Intermediate')
    ADVANCE = 'Advance', _('Advanced')

class GenderChoices(TextChoices):
    MALE = 'M', _('Male')
    FEMALE = 'F', _('Female')

class GoalChoices(TextChoices):
    LOSE =  'Lose', _('Lose Weight')
    GAIN = 'Gain', _('Gain Weight')
    MAINTAIN = 'Maintain', _('Maintain Weight')