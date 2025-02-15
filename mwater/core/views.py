from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from .utils import generate_otp, send_otp
from django.contrib.auth.hashers import make_password
from rest_framework import permissions

class UserCreateAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({"detail": "User with this phone number already exists."}, status=status.HTTP_400_BAD_REQUEST)
        otp = generate_otp()
        send_otp(phone_number, otp)
        request.session['otp'] = otp
        request.session['phone_number'] = phone_number
        return Response({"detail": "OTP sent successfully."}, status=status.HTTP_201_CREATED)

class UserDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, phone_number):
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user)
        return Response(serializer.data)

class VerifyOTPAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        if 'otp' not in request.session or request.session['otp'] != int(otp):
            return Response({"detail": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
        if request.session['phone_number'] != phone_number:
            return Response({"detail": "Phone number does not match."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create(
            phone_number=phone_number,
            password=make_password(request.data.get('password')),  
        )
        del request.session['otp']
        del request.session['phone_number']
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)