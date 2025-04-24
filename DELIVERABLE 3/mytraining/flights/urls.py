from django.urls import path
from . import views  # Import views from the current app
from .views import CustomLoginView  # Import the custom login view

# Define URL patterns for the 'flights' app
urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('enroll/<int:module_id>/', views.enroll, name='enroll'),  # Enroll in a module
    path('register/', views.register, name='register'),  # User registration
    path('trainer/', views.trainer_dashboard, name='trainer_dashboard'),  # Trainer dashboard
    path('coordinator/', views.coordinator_dashboard, name='coordinator_dashboard'),  # Coordinator dashboard
    path('module/<int:module_id>/', views.module_video, name='module_video'),  # video page for a module
    path('accounts/login/', CustomLoginView.as_view(), name='login'),  # Login page
]
