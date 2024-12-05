from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Endpoint for myfitapp
    path('', include('myfitapp.urls')),
    # Endpoint for authentication
    path('auth/', include('authentication.urls')),
]
