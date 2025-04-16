from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q

from myfitapp.choices import LevelChoices
from authentication.models import Profile
from myfitapp.pagination import CustomPageNumberPagination
from myfitapp.models import (CardioTraining, CrossFitTraining,
    FlexibilityTraining, PersonalWorkoutPlan, Recovery,
    ResistanceTraining, UserFoodLog, PersonalDietPlan,)
from myfitapp.serializers import ( RecipeSerializer,
    CardioTrainingSerializer, CrossFitTrainingSerializer,
    FlexibilityTrainingSerializer, SearchSerializer,
    RecoverySerializer, PersonalWorkoutPlanSerializer,
    UserFoodLogSerializer, ResistanceTrainingSerializer,
    PersonalDietPlanSerializer,)
from myfitapp.helper import daily_summary
from myfitapp.scripts import (calculate_end_date,
    nutritional_facts, recipe_recommendation,)


# View to search a food to check calories
class SearchFoodView(APIView):
    """
    This view will use an API to get the nutritional information
    like calories, fats, protein, sugars, sodium things like that,
    about the food
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_serializer = SearchSerializer(data=request.data)
        print(request.data)
        if input_serializer.is_valid():
            food_name = input_serializer.validated_data["food_name"].title()
            quantity = input_serializer.validated_data["quantity"]

            return Response(nutritional_facts(food_name, quantity))
        raise ValidationError(detail="Not Valid")


# View to search a recipe
class SearchRecipe(APIView):
    """
    This View uses an API to give the recipe of the dish
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_serializer = RecipeSerializer(data=request.data)
        if input_serializer.is_valid():
            food_name = input_serializer.validated_data["food_name"]

            return Response(recipe_recommendation(food_name))
        raise ValidationError(detail="Not Valid")


# View to list all the foods logged that day
class ListFoodsView(APIView):
    """
    The user can see all the foods they consumed on that day
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_date = request.query_params.get("date", timezone.now().date())

        try:
            query_date = timezone.now().date().fromisoformat(str(query_date))
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."}, status=400
            )

        foods = UserFoodLog.objects.filter(
            profile=request.user.profile, date=query_date
        )
        serializer = UserFoodLogSerializer(foods, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# View to track the user calories
class UserFoodLogView(APIView):
    """
    View to log the food, it also shows how much calorie is remaining
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_serializer = UserFoodLogSerializer(data=request.data)
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile not found for the user."},
                status=status.HTTP_404_NOT_FOUND,
            )
        summary = daily_summary(profile)

        if input_serializer.is_valid():
            input_serializer.save(profile=profile)

            return Response(
                {
                    "daily_summary": summary,
                    "food_log": input_serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile not found for the user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        food_logs = UserFoodLog.objects.filter(
            profile=profile, date=timezone.now().date()
        )
        serializer = UserFoodLogSerializer(food_logs, many=True)
        summary = daily_summary(profile)

        return Response(
            {
                "daily_summary": summary,
                "food_log": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request):
        # Check for food_name in request data
        food_name = request.data.get("food_name")
        if not food_name:
            return Response(
                {"error": "Food name must be provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            profile = request.user.profile
        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile not found for the user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        log_date = request.data.get("date", timezone.now().date())

        try:
            log = UserFoodLog.objects.filter(
                profile=profile, date=log_date, food_name=food_name
            )
            log.delete()

            return Response(
                {"detail": f"{food_name} - deleted successfully."},
                status=status.HTTP_200_OK,
            )
        except UserFoodLog.DoesNotExist:
            return Response(
                {"error": f"Food log for '{food_name}' not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


# View to create a custom diet plan for each user
class PersonalDietPlanView(APIView):
    """
    This View gives a custom diet plan with appropriate macros
    """

    permission_classes = [IsAuthenticated]

    # get the diet plan of the user
    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            diet_plan = PersonalDietPlan.objects.filter(profile=profile)
            serializer = PersonalDietPlanSerializer(diet_plan, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile not found for the user."},
                status=status.HTTP_404_NOT_FOUND,
            )


# View to list Resistance Training Wrokouts
class ResistanceTrainingView(APIView):
    """
    This View lists all the resistance trainings so the user can
    add them in their personal workout plan
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        muscle_group = request.query_params.get("muscle_group")
        training_level = request.query_params.get("training_level")
        exercises = ResistanceTraining.objects.all()

        if muscle_group:
            exercises = exercises.filter(muscle_group__name=muscle_group)
        if training_level:
            exercises = exercises.filter(current_level__current_level=training_level)

        paginator = CustomPageNumberPagination()
        paginated_exercises = paginator.paginate_queryset(exercises, request)

        serializer = ResistanceTrainingSerializer(paginated_exercises, many=True)
        return paginator.get_paginated_response(serializer.data)


# View to list Cardio-Vascular Workouts
class CardioTrainingView(APIView):
    """
    This View lists all the cardio trainings so the user can
    add them in their personal workout plan
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        training_level = request.query_params.get("training_level")
        exercises = CardioTraining.objects.all()

        if training_level:
            exercises = exercises.filter(current_level__current_level=training_level)

        paginator = CustomPageNumberPagination()
        paginated_exercises = paginator.paginate_queryset(exercises, request)

        serializer = CardioTrainingSerializer(paginated_exercises, many=True)
        return paginator.get_paginated_response(serializer.data)


# View to list CrossFit Workouts
class CrossFitTrainingView(APIView):
    """
    This View lists all the crossfit trainings so the user can
    add them in their personal workout plan
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        training_level = request.query_params.get("training_level")
        exercises = CrossFitTraining.objects.all()

        if training_level:
            exercises = exercises.filter(current_level__current_level=training_level)

        paginator = CustomPageNumberPagination()
        paginated_exercises = paginator.paginate_queryset(exercises, request)

        serializer = CrossFitTrainingSerializer(paginated_exercises, many=True)
        return paginator.get_paginated_response(serializer.data)


# View to list Flexibility Training
class FlexibilityTrainingView(APIView):
    """
    This View lists all the flexibility trainings so the user can
    add them in their personal workout plan
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        stretches = FlexibilityTraining.objects.all()

        paginator = CustomPageNumberPagination()
        paginated_stretches = paginator.paginate_queryset(stretches, request)

        serializer = FlexibilityTrainingSerializer(paginated_stretches, many=True)
        return paginator.get_paginated_response(serializer.data)


# View to list Recovery Methods
class RecoveryView(APIView):
    """
    This View lists all the recovery methods so the user can
    add them in their personal workout plan
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        methods = Recovery.objects.all()
        paginator = CustomPageNumberPagination()
        paginated_methods = paginator.paginate_queryset(methods, request)

        serializer = RecoverySerializer(paginated_methods, many=True)
        return paginator.get_paginated_response(serializer.data)


# API View for managing personal workout plans.
class PersonalWorkoutPlanView(APIView):
    """
    In this view user can create their own personalized workout
    plans and list them or delete them
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PersonalWorkoutPlanSerializer(
            data=request.data, context={"request": request}
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            profile = request.user.profile
            level = serializer.validated_data.get("level")
            workout_type = serializer.validated_data.get("workout_type")
            start_date = serializer.validated_data.get("start_date")
            end_date = serializer.validated_data.get("end_date")

            workout_mapping = {
                "Resistance": "resistance_trainings",
                "Cardio": "cardio_trainings",
                "CrossFit": "crossfit_trainings",
                "Flexibility": "flexibility_trainings",
                "Recovery": "recoveries",
            }

            field_name = workout_mapping.get(workout_type)

            existing_plan = PersonalWorkoutPlan.objects.filter(
                profile=profile,
                **{f"{field_name}__current_level": level},
            ).first()

            if existing_plan:
                return Response(
                    {
                        "message": f"A {workout_type} workout plan for level '{level}' already exists."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            workout_plan, created = PersonalWorkoutPlan.objects.get_or_create(
                profile=profile,
                end_date__isnull=True,
                defaults={"start_date": start_date or timezone.now().date()},
            )

            self._assign_workouts_by_type_and_level(workout_plan, workout_type, level)

            if end_date:
                workout_plan.end_date = end_date
            elif created:
                workout_plan.end_date = calculate_end_date(workout_plan.start_date)

            workout_plan.save()
            return Response(
                {"message": "Workout plan created successfully."},
                status=status.HTTP_201_CREATED,
            )

        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile not found for the user."},
                status=status.HTTP_404_NOT_FOUND,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            # Fetch workout plans for the authenticated user
            workout_plans = PersonalWorkoutPlan.objects.filter(
                profile=request.user.profile
            )

            if not workout_plans:
                return Response(
                    {"message": "No workout plans found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            serializer = PersonalWorkoutPlanSerializer(workout_plans, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile not found for the user."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def delete(self, request):

        level = request.data.get("level")
        workout_type = request.data.get("workout_type")

        if level not in [choice[0] for choice in LevelChoices.choices]:
            return Response(
                {"detail": "Invalid level."}, status=status.HTTP_400_BAD_REQUEST
            )

        if workout_type not in [
            "Resistance",
            "Cardio",
            "CrossFit",
            "Flexibility",
            "Recovery",
        ]:
            return Response(
                {"detail": "Invalid workout type."}, status=status.HTTP_400_BAD_REQUEST
            )

        workout_mapping = {
            "Resistance": "resistance_trainings",
            "Cardio": "cardio_trainings",
            "CrossFit": "crossfit_trainings",
            "Flexibility": "flexibility_trainings",
            "Recovery": "recoveries",
        }

        field_name = workout_mapping.get(workout_type)

        workout_plan = PersonalWorkoutPlan.objects.filter(profile=request.user.profile)

        if workout_type in workout_mapping:
            workout_plan = workout_plan.filter(
                Q(**{f"{field_name}__current_level": level})
                & ~Q(**{f"{field_name}__isnull": True})
            )

        if not workout_plan.exists():
            return Response(
                {"detail": f"No {workout_type} workout plans found for level {level}."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Delete the filtered workout plans
        workout_plan.delete()

        return Response(
            {"detail": f"{workout_type} workout plan deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )

    # Helper method to add workouts in personal workout plan
    def _assign_workouts_by_type_and_level(self, workout_plan, workout_type, level):
        workout_mapping = {
            "Resistance": ResistanceTraining,
            "Cardio": CardioTraining,
            "CrossFit": CrossFitTraining,
            "Flexibility": FlexibilityTraining,
            "Recovery": Recovery,
        }

        if workout_type in workout_mapping:
            workout_model = workout_mapping[workout_type]
            workouts = workout_model.objects.filter(current_level=level)

            if workout_type == "Resistance":
                workout_plan.resistance_trainings.set(workouts)
            elif workout_type == "Cardio":
                workout_plan.cardio_trainings.set(workouts)
            elif workout_type == "CrossFit":
                workout_plan.crossfit_trainings.set(workouts)
            elif workout_type == "Flexibility":
                workout_plan.flexibility_trainings.set(workouts)
            elif workout_type == "Recovery":
                workout_plan.recoveries.set(workouts)
        else:
            raise ValueError(f"Invalid workout type: {workout_type}")
