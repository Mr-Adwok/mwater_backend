from rest_framework import serializers
from .models import User, Bill

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'phone_number', 'is_verified']

class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['id', 'user', 'water_account_id', 'meter_photo', 'payment_fee', 'is_paid', 'created_at']