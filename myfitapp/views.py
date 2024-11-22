import rest_framework.pagination
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework import status, mixins, generics
from rest_framework.response import Response
from datetime import date

from .scripts import nutritional_facts, recipe_recommendation
from .pagination import CustomPageNumberPagination
from .models import (
    BodyMetrics,
    CardioTraining,
    CrossFitTraining,
    FlexibilityTraining,
    PersonalWorkoutPlan,
    Profile,
    Recovery,
    ResistanceTraining,
    UserFoodLog,
)
from .serializers import (
    BodyMetricsSerializer,
    CardioTrainingSerializer,
    CrossFitTrainingSerializer,
    FlexibilityTrainingSerializer,
    PersonalDietPlanSerializer,
    RecipeSerializer,
    RecoverySerializer,
    ResistanceTrainingSerializer,
    SearchSerializer,
    UserFoodLogSerializer,
    UserSerializer,
)


# View to Register the User
class UserRegisterView(mixins.CreateModelMixin, GenericAPIView):
    """
    View for user registration. This view allows unauthenticated users to
    register by creating a new user profile.
    """

    permission_classes = [AllowAny]
    queryset = Profile.objects.all()
    serializer_class = UserSerializer

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


# View to update the body metrics of the user
class BodyMetricsUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BodyMetricsSerializer

    def get_object(self):
        # Retrieve the user's profile
        profile = self.request.user.profile

        body_metrics, created = BodyMetrics.objects.get_or_create(
            profile=profile,
            defaults={
                "weight": self.request.data.get("weight", 0),
            },
        )

        if created and not body_metrics.weight:
            raise ValidationError("Weight is required for new entries.")

        return body_metrics


# View to track the user calories
class FoodLogCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserFoodLogSerializer
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return UserFoodLog.objects.filter(profile=self.request.user.profile)

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)


# View to search a food to check calories
class SearchFoodView(APIView):
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        input_serializer = RecipeSerializer(data=request.data)
        if input_serializer.is_valid():
            food_name = input_serializer.validated_data["food_name"]

            return Response(recipe_recommendation(food_name))
        raise ValidationError(detail="Not Valid")


# View to list all the foods logged that day
class ListFoodsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query_date = request.query_params.get("date", date.today())

        try:
            query_date = date.fromisoformat(str(query_date))
        except ValueError:
            return Response(
                {"error": "Invalid date format. Use YYYY-MM-DD."}, status=400
            )

        foods = UserFoodLog.objects.filter(
            profile=request.user.profile, date=query_date
        )
        serializer = UserFoodLogSerializer(foods, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# View to list Resistance Training Wrokouts
class ResistanceTrainingView(APIView):
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
    permission_classes = [IsAuthenticated]

    def get(self, request):
        stretches = FlexibilityTraining.objects.all()

        paginator = CustomPageNumberPagination()
        paginated_stretches = paginator.paginate_queryset(stretches, request)

        serializer = FlexibilityTrainingSerializer(paginated_stretches, many=True)
        return paginator.get_paginated_response(serializer.data)


# View to list Recovery Methods
class RecoveryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        methods = Recovery.objects.all()

        paginator = CustomPageNumberPagination()
        paginated_methods = paginator.paginate_queryset(methods, request)

        serializer = RecoverySerializer(paginated_methods, many=True)
        return paginator.get_paginated_response(serializer.data)


# View to create a custom workout plan for each user
class PersonalWorkoutPlanView(APIView):
    pass
