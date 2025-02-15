import requests
import random
from django.core.cache import cache


def send_otp(phone_number, otp):
    url = "https://api.africastalking.com/version1/messaging"
    headers = {
        "apiKey": "YOUR_API_KEY",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "username": "YOUR_USERNAME",
        "to": phone_number,
        "message": f"Your OTP is {otp}",
    }
    response = requests.post(url, headers=headers, data=data)
    return response.status_code == 201

def generate_otp():
    return random.randint(100000, 999999)

def store_otp(phone_number, otp):
    cache.set(phone_number, otp, timeout=300) 

def get_otp(phone_number):
    return cache.get(phone_number)

def send_payment_sms(phone_number, payment_fee):
    """
    Send an SMS with the payment fee and USSD code using Africa's Talking API.
    """
    ussd_code = "*123#"
    message = f"Your water bill payment fee is {payment_fee}. Pay using USSD code: {ussd_code}"

    url = "https://api.africastalking.com/version1/messaging"
    headers = {
        "apiKey": "YOUR_API_KEY",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "username": "YOUR_USERNAME",
        "to": phone_number,
        "message": message,
    }
    response = requests.post(url, headers=headers, data=data)
    return response.status_code == 201

def calculate_payment_fee(water_consumption=None, user=None):
    """
    Calculate the payment fee dynamically based on water consumption or user details.
    """
    base_fee = 300 
    if water_consumption:
        consumption_fee = water_consumption * 10
        total_fee = base_fee + consumption_fee
    else:
        total_fee = base_fee

    if user and user.location == "premium":
        total_fee += 200

    return total_fee