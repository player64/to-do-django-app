from django.urls import path
from .views import CreateUserView
from users import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='user-register'),
    path('login/', jwt_views.TokenObtainPairView.as_view(), name='user-login'),
    path('logout/', views.ApiLogout.as_view(), name='user-logout'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token-refresh')
]
