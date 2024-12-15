from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Fitness Tracker API",
      default_version='v1',
      description="API documentation for the Fitness Tracker application",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="pavankumar.v1301@gmail.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    # Endpoint for myfitapp
    path('api/', include('myfitapp.urls')),
    # Endpoint for authentication
    path('auth/', include('authentication.urls')),
    # API documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    path('', schema_view.with_ui('redoc', cache_timeout=0), name='redoc-schema'),

]