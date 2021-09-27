from rest_framework import permissions, status
from rest_framework.views import APIView
from accounts.serializers import *
from rest_framework.authtoken.models import Token, TokenProxy
from google.oauth2 import id_token
from google.auth.transport import requests
from accounts.models import *
from sgspl_base import settings
from rest_framework.response import Response


class SocialLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        social_token = request.data['social_token']
        profile = social_profile(token=social_token)
        return Response(profile)


def social_profile(token):
    client_id = settings.CLIENT_ID
    try:
        ctx = {}
        # Specify the CLIENT_ID of the app that accesses the backend:
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), client_id)
        email = idinfo['email']
        user = User.objects.filter(email=email).last()
        if user:
            # genrate token
            token = Token.objects.get(user=user)

            ctx['user'] = user.pk,
            ctx['token'] = token.key

            return ctx
        else:
            first_name, last_name = idinfo['given_name'], idinfo['family_name']
            email = idinfo['email']
            user = User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email)
            user.set_password(token[0:10])
            user.save()

            # creating profile
            profile = Profile.objects.create(created_by=user, updated_by=user)

            # genrate token
            token = Token.objects.create(user=user)

            ctx['user'] = user.pk,
            ctx['token'] = token.key

            return ctx

    except ValueError as e:
        # Invalid token
        print(e)
        ctx = {
            'message': 'Invalid Crediantial. Please create your account first.'
        }
        return ctx
