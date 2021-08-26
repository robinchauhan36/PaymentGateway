from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from accounts.serializers import *
from rest_framework.response import Response
from sgspl_base import settings
import random


# Create your views here.
class RegistrationAPI(GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            payload = request.data.copy()
            payload['created_by'] = user['user']
            payload['updated_by'] = user['user']
            serializer = ProfileSerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(user)
            return Response(serializer.errors)
        return Response(serializer.errors)


class UserLoginAPI(GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get or Generate token
        token, created = Token.objects.get_or_create(
            user=serializer.validated_data['user'])
        request = {
            'user': serializer.validated_data['user']
        }
        response_serializer = UserLoginReplySerializer(token, context={'request': request})
        return Response(response_serializer.data)


class PasswordChangeAPI(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        password = request.data.get("password")
        confirmPassword = request.data.get("confirmPassword")

        if password != confirmPassword:
            return Response({'error': 'Password does not match'},
                            status=500)

        user = User.objects.get(pk=request.user.pk)
        user.set_password(password)
        user.save()
        return Response({'ok': 'Password changed successfully! '},
                        status=200)


class OTPView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        user = User.objects.filter(email=request.data['email']).last()
        if user:
            otp = random.randint(1111, 9999)
            try:
                subject = 'SocialMarketing'
                message = f'Hi {user.username}, Here is OTP from SocialMarketing.\n{otp}'
                email_from = settings.EMAIL_HOST_USER
                recipient_list = [user.email, ]
                send_mail(subject, message, email_from, recipient_list)
            except Exception as e:
                print('send email.')
            model_data = request.data.copy()
            model_data['otp'] = otp
            model_data['created_by'] = user.pk
            model_data['updated_by'] = user.pk
            serializer = OTPSerializer(data=model_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response({'message': 'There is no user register with this email.'})

    def put(self, request):
        user = User.objects.filter(email=request.data['email']).last()
        if user:
            query_otp = Otp.objects.filter(user=user.id).last()
            if query_otp:
                query_data = {
                    'verify': 'true'
                }
                if int(request.data['otp']) == int(query_otp.otp):
                    query_update = OTPSerializer(query_otp, data=query_data)
                    if query_update.is_valid():
                        query_update.save()
                        return Response({'message': 'you have successfully verify OTP.'}, status=status.HTTP_200_OK)
                    return Response({'message': query_update.errors}, status=status.HTTP_400_BAD_REQUEST)
                return Response({'message': 'OTP that you enter is not valid.', 'status': 400},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response({'message': 'Please send OTP first.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'There is no user register with this email.'}, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = (permissions.AllowAny,)

    def put(self, request):
        user = User.objects.filter(email=request.data['email']).last()
        if user:
            query_otp = Otp.objects.filter(created_by=user.id, verify='true').last()
            if query_otp:
                user.set_password(request.data['password'])
                user.save()
                # remove previous otp
                inst = Otp.objects.filter(created_by=user).delete()
                return Response({'message': 'You have successfully reset your password.'}, status=status.HTTP_200_OK)
            return Response({'message': 'First Verify OTP then reset your password'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'There is no user register with this email.'}, status=status.HTTP_400_BAD_REQUEST)
