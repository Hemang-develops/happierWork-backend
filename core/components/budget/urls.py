from django.urls import path
from .views import read_data, create_data, update_data, delete_data

urlpatterns = [
    path('data/', read_data, name='read_data'),
    path('data/add/', create_data, name='create_data'),
    path('data/update/<str:entry_id>/', update_data, name='update_data'),
    path('data/delete/<str:entry_id>/', delete_data, name='delete_data'),
]
