from django.urls import path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core import views


urlpatterns = [
    path("", TemplateView.as_view(
        template_name="core/index.html")),
    path('api/auth/register/', views.UserRegisterView.as_view(), name="auth-register"),
    path('api/auth/login/', views.UserLoginView.as_view(), name="auth-login"),
    path('api/auth/token_refresh/', views.UserTokenRefreshView.as_view(),
         name="auth-token-refresh"),
]
