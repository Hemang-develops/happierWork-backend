from django.urls import path
from .views import login_view  # Import the function-based view

urlpatterns = [
    path('api/login/', login_view, name='login'),  # Use the function directly
]
