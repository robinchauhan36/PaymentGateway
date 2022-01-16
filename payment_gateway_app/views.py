import random
import string
from rest_framework.response import Response
from .serializer import *
from .models import *
from rest_framework import permissions, viewsets


# Create your views here.

class UserPaymentViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PaymentDetailSerializer
    queryset = PaymentDetail

    def list(self, request, *args, **kwargs):
        query = PaymentDetail.objects.filter(user=request.user, status='success')
        serializer = PaymentSerializer(query, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = PaymentSerializer(data=data)
        if serializer.is_valid():
            authorization_code = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(12))
            serializer.save(status='success', authorization_code=authorization_code)
            return Response({'payment_data': serializer.data,
                             "card": {'number': request.data['card'][0]['number']}})
        return Response(serializer.errors)
