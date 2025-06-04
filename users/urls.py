from django.urls import path
from .views import UserRegistrationAPIView, CustomAuthTokenLoginAPIView, UserLogoutAPIView, UserDetailAPIView

urlpatterns = [
    path('register/', UserRegistrationAPIView.as_view(), name='user-register'),
    path('login/', CustomAuthTokenLoginAPIView.as_view(), name='user-login'),
    path('logout/', UserLogoutAPIView.as_view(), name='user-logout'),
    path('me/', UserDetailAPIView.as_view(), name='user-detail'),
]
