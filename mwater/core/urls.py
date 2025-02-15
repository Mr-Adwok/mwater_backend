from django.urls import path
from .views import UserCreateAPIView, UserDetailAPIView

urlpatterns = [
    path('api/users/', UserCreateAPIView.as_view(), name='user-create'),
    path('api/users/<str:phone_number>/', UserDetailAPIView.as_view(), name='user-detail'),
]
