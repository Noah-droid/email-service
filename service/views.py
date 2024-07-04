from django.core.mail import send_mail
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from .models import OTP
from .serializers import OTPSendSerializer, OTPVerifySerializer, EmailSerializer
import secrets
import string
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class SendOTP(APIView):
    @swagger_auto_schema(
        request_body=OTPSendSerializer,
        responses={
            200: openapi.Response('OTP sent successfully'),
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = OTPSendSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = ''.join(secrets.choice(string.digits) for i in range(6))
            
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            OTP.objects.create(email=email, otp=otp)
            
            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTP(APIView):
    @swagger_auto_schema(
        request_body=OTPVerifySerializer,
        responses={
            200: openapi.Response('OTP verified successfully'),
            400: 'Invalid OTP or OTP expired'
        }
    )
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            
            try:
                otp_instance = OTP.objects.get(email=email, otp=otp, is_used=False)
                
                if timezone.now() > otp_instance.created_at + timezone.timedelta(minutes=10):
                    return Response({'message': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)
                
                otp_instance.is_used = True
                otp_instance.save()
                
                return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
            except OTP.DoesNotExist:
                return Response({'message': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SendEmail(APIView):
    @swagger_auto_schema(
        request_body=EmailSerializer,
        responses={
            200: openapi.Response('Email sent successfully'),
            400: 'Bad Request'
        }
    )
    def post(self, request):
        serializer = EmailSerializer(data=request.data)
        if serializer.is_valid():
            to_email = serializer.validated_data['to_email']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [to_email],
                fail_silently=False,
            )
            
            return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
