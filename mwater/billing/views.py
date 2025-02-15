from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage
from .models import User, Bill
from .serializers import UserSerializer, BillSerializer
from .utils import send_otp, generate_otp, store_otp, get_otp, calculate_payment_fee, send_payment_sms

class SignupAPIView(APIView):
    def post(self, request):
        name = request.data.get('name')
        phone_number = request.data.get('phone_number')
        if not name or not phone_number:
            return Response({'error': 'Name and phone number are required'}, status=status.HTTP_400_BAD_REQUEST)

        otp = generate_otp()
        store_otp(phone_number, otp)
        send_otp(phone_number, otp)

        user = User.objects.create(name=name, phone_number=phone_number)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class VerifyOTPAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        stored_otp = get_otp(phone_number)

        if not stored_otp or int(otp) != stored_otp:
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(phone_number=phone_number)
        user.is_verified = True
        user.save()
        return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)

class LoginAPIView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        if not phone_number:
            return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)

        otp = generate_otp()
        store_otp(phone_number, otp)
        send_otp(phone_number, otp)

        return Response({'message': 'OTP sent to your phone number'}, status=status.HTTP_200_OK)

class PayBillAPIView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        water_account_id = request.data.get('water_account_id')
        meter_photo = request.FILES.get('meter_photo')

        if not user_id or not water_account_id or not meter_photo:
            return Response({'error': 'User ID, water account ID, and meter photo are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.get(id=user_id)
        photo_path = default_storage.save(f'meter_photos/{meter_photo.name}', meter_photo)

        payment_fee = calculate_payment_fee()
        bill = Bill.objects.create(
            user=user,
            water_account_id=water_account_id,
            meter_photo=photo_path,
            payment_fee=payment_fee,
        )

        send_payment_sms(user.phone_number, payment_fee)

        serializer = BillSerializer(bill)
        return Response(serializer.data, status=status.HTTP_201_CREATED)