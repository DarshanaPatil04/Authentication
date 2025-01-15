from django.contrib import admin
from django.urls import path, include
from auth_app import views  # Correct import


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('auth_app.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include('auth_app.urls')), # Include app urls
    


]
