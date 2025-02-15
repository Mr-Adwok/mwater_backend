from django.urls import path
from .views import SignupAPIView, VerifyOTPAPIView, LoginAPIView, PayBillAPIView

urlpatterns = [
    path('api/signup/', SignupAPIView.as_view(), name='signup'),
    path('api/verify-otp/', VerifyOTPAPIView.as_view(), name='verify_otp'),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/pay-bill/', PayBillAPIView.as_view(), name='pay_bill'),
]