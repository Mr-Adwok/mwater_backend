from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone, name, password=None):
        if not phone:
            raise ValueError("Users must have a phone number")
        user = self.model(phone=phone, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    phone = models.CharField(max_length=15, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def _str_(self):
        return self.phone


class OTP(models.Model):
    phone = models.CharField(max_length=15, unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.phone} - {self.code}"


class BillPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    water_account_id = models.CharField(max_length=50)
    meter_photo = models.ImageField(upload_to="meter_photos/")
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    ussd_code = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[("pending", "Pending"), ("paid", "Paid")], default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Payment {self.id} - {self.status}"