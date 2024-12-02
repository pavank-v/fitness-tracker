from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import ValidationError
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from django.utils import timezone

from myfitapp.scripts import (calculate_end_date, nutritional_facts,
    recipe_recommendation,
)
from myfitapp.pagination import CustomPageNumberPagination
from myfitapp.models import (BodyMetrics, CardioTraining, CrossFitTraining,
    FlexibilityTraining, PersonalWorkoutPlan, Profile, Recovery,
    ResistanceTraining, UserFoodLog, PersonalDietPlan,
)
from myfitapp.serializers import (BodyMetricsSerializer, RecipeSerializer, 
    CardioTrainingSerializer, CrossFitTrainingSerializer,
    FlexibilityTrainingSerializer, SearchSerializer, RecoverySerializer,
    PersonalWorkoutPlanSerializer,  UserSerializer, UserFoodLogSerializer,
    ResistanceTrainingSerializer, PersonalDietPlanSerializer,
)


# View to Register the User
class UserRegisterView(
    mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericAPIView
):
    """
    View for user registration. This view allows unauthenticated users to
    register by creating a new user profile.
    """

    permission_classes = [AllowAny]
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        elif self.request.method in ["PUT", "PATCH"]:
            return [IsAuthenticated()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        response.data = {
            "Message": "User created successfully!!!",
            "User-ID": response.data.get("id"),
            "Profile-data": response.data.get("profile"),
            "Additional-info": "Thanks for signing up",
        }
        return response

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return response

    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data

        allowed_fields = [
            "age",
            "gender",
            "weight",
            "height",
            "current_level",
            "body_fat_percentage",
            "goal",
        ]

        for field in allowed_fields:
            if field in data:
                setattr(instance, field, data[field])

        instance.save()

        return Response(
            {
                "message": "Profile Updated Successfully",
                "updated_data": {
                    field: getattr(instance, field)
                    for field in allowed_fields
                    if hasattr(instance, field)
                },
            },
            status=status.HTTP_200_OK,
        )


# View to update the body metrics of the user
class BodyMetricsUpdateView(generics.RetrieveUpdateAPIView):
    """
    With this view user can update the body metrics to
    keep track of their progress
    """

    permission_classes = [IsAuthenticated]
    serializer_class = BodyMetricsSerializer

    def get_object(self):
        try:
            profile = self.request.user.profile
        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile not found for the user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        body_metrics, created = BodyMetrics.objects.get_or_create(
            profile=profile,
            defaults={
                "weight": self.request.data.get("weight", 0),
            },
        )

        if created and not body_metrics.weight:
            raise ValidationError("Weight is required for new entries.")

        return body_metrics


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

        if input_serializer.is_valid():
            input_serializer.save(profile=profile)

            daily_summary = UserFoodLog.daily_summary(profile)

            return Response(
                {
                    "message": "Food Logged Successfully",
                    "food-log": input_serializer.data,
                    "daily_summary": {
                        "total_calories": daily_summary["total_calories"],
                        "total_protein": daily_summary["total_protein"],
                        "total_carbs": daily_summary["total_carbs"],
                        "total_fats": daily_summary["total_fats"],
                        "remaining_calories": daily_summary["remaining_calories"],
                    },
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
        daily_summary = UserFoodLog.daily_summary(profile)

        return Response(
            {
                "daily_summary": daily_summary,
                "food-log": serializer.data,
            },
            status=status.HTTP_200_OK,
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


# View to create a custom workout plan for each user
class PersonalWorkoutPlanView(APIView):
    """
    This view will show the user's workout plan
    """

    permission_classes = [IsAuthenticated]

    # get the workouts of a perticular user
    def get(self, request):
        try:
            profile = Profile.objects.get(user=request.user)
            workout_plans = PersonalWorkoutPlan.objects.filter(profile=profile)
            serializer = PersonalWorkoutPlanSerializer(workout_plans, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile not found for the user."},
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request):
        serializer = PersonalWorkoutPlanSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        resistance_trainings = serializer.validated_data.get(
            "resistance_trainings_ids", []
        )
        cardio_trainings = serializer.validated_data.get("cardio_trainings_ids", [])
        crossfit_trainings = serializer.validated_data.get("crossfit_training_ids", [])
        flexibility_trainings = serializer.validated_data.get(
            "flexibility_trainings_ids", []
        )
        recoveries = serializer.validated_data.get("recovery_ids", [])
        end_date = serializer.validated_data.get("end_date")

        try:
            profile = Profile.objects.get(user=request.user)

            # Get or create the active workout plan
            workout_plan, created = PersonalWorkoutPlan.objects.get_or_create(
                profile=profile,
                end_date__isnull=True,
                defaults={"start_date": timezone.now().date()},
            )

            # Update workouts in the plan
            if resistance_trainings:
                workout_plan.resistance_trainings.add(*resistance_trainings)
            if cardio_trainings:
                workout_plan.cardio_trainings.add(*cardio_trainings)
            if crossfit_trainings:
                workout_plan.crossfit_trainings.add(*crossfit_trainings)
            if flexibility_trainings:
                workout_plan.flexibility_trainings.add(*flexibility_trainings)
            if recoveries:
                workout_plan.recoveries.add(*recoveries)

            # Set or calculate the end_date
            if end_date:
                workout_plan.end_date = end_date
            elif created:  # Only calculate end_date for a new plan
                workout_plan.end_date = calculate_end_date(workout_plan.start_date)

            workout_plan.save()

            return Response(
                {"message": "Workout plan created/updated successfully."},
                status=status.HTTP_201_CREATED,
            )

        except Profile.DoesNotExist:
            return Response(
                {"error": "Profile not found for the user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
