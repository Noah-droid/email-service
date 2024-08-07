# The above code defines Django API views for sending OTP via email, verifying OTP, and sending
# general emails.
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
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
            
            # Render the email template
            html_content = render_to_string('otp_email.html', {'email': email, 'otp': otp})
            text_content = strip_tags(html_content)
            
            # Send OTP via email
            msg = EmailMultiAlternatives(
                'Your OTP Code',
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            # Save OTP in database
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
            toEmail = serializer.validated_data['toEmail']
            subject = serializer.validated_data['subject']
            message = serializer.validated_data['message']
            
            # Render the HTML content
            html_content = render_to_string('general_email.html', {'message': message})
            text_content = strip_tags(html_content)
            
            msg = EmailMultiAlternatives(
                subject,
                text_content,
                settings.DEFAULT_FROM_EMAIL,
                [toEmail]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            
            return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



