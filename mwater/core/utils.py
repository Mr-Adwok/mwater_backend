import random
from africastalking import Sms
from django.conf import settings

def initialize_africastalking():
    africastalking = Sms
    africastalking.initialize(settings.AFRICASTALKING_USERNAME, settings.AFRICASTALKING_API_KEY)
    return africastalking

def generate_otp():
    otp = random.randint(100000, 999999)
    return otp

def send_otp(phone_number, otp):
    africastalking = initialize_africastalking()
    message = f"Your verification code is {otp}. Please use this to complete your registration."
    try:
        response = africastalking.send(message, [phone_number])
        return response
    except Exception as e:
        return str(e)
