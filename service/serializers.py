from rest_framework import serializers
from .models import OTP

class EmailSerializer(serializers.Serializer):
    toEmail = serializers.EmailField()
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField()


class OTPSendSerializer(serializers.Serializer):
    email = serializers.EmailField()

class OTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
