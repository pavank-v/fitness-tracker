from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework import status, mixins
from rest_framework.response import Response

from authentication.models import Profile
from authentication.serializers import UserSerializer


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

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(self.request.user)
        return Response(serializer.data)

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
