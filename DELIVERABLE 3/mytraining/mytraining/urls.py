from django.contrib import admin
from django.urls import path, include
from flights.views import CustomLoginView  # Use custom login
from django.contrib.auth.views import LogoutView  # Use built-in logout

# All the links for the site
urlpatterns = [
    path('admin/', admin.site.urls),  # Admin page
    path('', include('flights.urls')),  # Links from flights app
    path('accounts/login/', CustomLoginView.as_view(), name='login'),  # Login page
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout'),  # Logout and go home
]
