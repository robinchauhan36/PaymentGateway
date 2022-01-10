from rest_framework.generics import GenericAPIView
from accounts.serializers import *
from rest_framework.response import Response


# Create your views here.
class RegistrationAPI(GenericAPIView):
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            payload = request.data.copy()
            payload['user'] = user['user']
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
