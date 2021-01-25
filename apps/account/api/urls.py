from django.urls import path
from .views import (CustomTokenObtainPairView, UserRetrieveAPIView)
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter

app_name = 'user_api'
router = DefaultRouter()

router.register('user_details', UserRetrieveAPIView, basename='user_details'),

urlpatterns = router.urls

urlpatterns += [
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
]
