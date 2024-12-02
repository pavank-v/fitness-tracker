from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from myfitapp.views import UserRegisterView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Endpoints for Authentication
    path('user/', UserRegisterView.as_view(), name='register'),
    path('api-auth/', include('rest_framework.urls')),
    # Endpoints for jwt
    path("token/", TokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    # Endpoint for myfitapp
    path('', include('myfitapp.urls'))
]
