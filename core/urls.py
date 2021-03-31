from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token  # <-- Here

from core import views

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),  # <-- And here
    path('register/', views.UserCreate.as_view()),
    path('weather/', views.CurrentWeatherApiView.as_view(), name='get-weather-info'),
]
