from django.contrib import admin
from .models import PersonalDietPlan, UserFoodLog

admin.site.register(PersonalDietPlan)
admin.site.register(UserFoodLog)