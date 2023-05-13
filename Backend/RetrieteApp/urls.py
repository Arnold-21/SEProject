from django.urls import path
from .views import *
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', myTokenObtainPariView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/register/', RegisterView.as_view()),
    path('api/register/confirm/<int:code>/', RegisterConfirmView.as_view()),
]