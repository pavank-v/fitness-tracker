from django.contrib import admin
from .models import Profile, PersonalDietPlan, UserFoodLog

admin.site.register(Profile)
admin.site.register(PersonalDietPlan)
admin.site.register(UserFoodLog)