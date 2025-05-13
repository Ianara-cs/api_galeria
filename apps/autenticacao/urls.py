from django.urls import path, include

from rest_framework_simplejwt.views import TokenBlacklistView, TokenObtainPairView, TokenRefreshView
from .routers import router

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name="access_token"),
    path('logout', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('refresh/', TokenRefreshView.as_view(), name="refresh_token"),
    path('api/', include(router.urls))
]