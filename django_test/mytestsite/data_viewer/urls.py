from django.urls import path
from . import views

urlpatterns = [
    path('view_data/', views.view_data, name='view_data'),
    path('view_map/', views.view_map, name='view_map'),
    path('api/data/', views.api_data, name='api_data'),
    path('api/map/', views.api_map, name='api_map'),
]