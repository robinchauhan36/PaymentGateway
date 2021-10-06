from rest_framework.response import Response
from rest_framework import status, permissions, views, viewsets
from payment_app.models import *
from payment_app.serializers import *
from sgspl_base import settings
from payment_app.stripe_view import *


# Create your views here.
class StripeAccountConnect(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = StripeAccountSerializer
    queryset = StripeAccount.objects.all()

    def list(self, request, *args, **kwargs):
        query = StripeAccount.objects.filter(created_by=request.user)
        if len(query) >= 1:
            return Response('Your account is already connect with stripe.', status=status.HTTP_208_ALREADY_REPORTED)
        return Response('Please connect your account with stripe.', status=status.HTTP_200_OK)

    def create(self, request):
        query = StripeAccount.objects.filter(created_by=request.user)
        if len(query) >= 1:
            return Response('Your account is already connect with stripe.', status=status.HTTP_208_ALREADY_REPORTED)

        payload = request.data.copy()
        account_id = generate_account_key(request.user.email)
        if account_id is None:
            return Response('There are some error occurred while connecting account, Please try again.')

        account_link = generate_account_link(account_id)
        payload['account_id'] = account_id
        payload['created_by'] = payload['updated_by'] = request.user.pk

        serializer = self.get_serializer(data=payload)
        if serializer.is_valid():
            serializer.save()
            return Response(account_link)
        return Response(serializer.error)


class SripePaymentCharge(viewsets.ModelViewSet):
    """
    payload = {
    "amount": 1,
    "expiry": "07/25",
    "card_number": "4242424242424242',
    "cvc": 786
    }
    """
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = PaymentHistorySerializer
    queryset = PaymentHistory.objects.all()

    def create(self, request, *args, **kwargs):
        charge_res = stripe_charge_create(expiry=request.data['expiry'], amount=request.data['amount'],
                                          card_number=request.data['card_number'], cvc=request.data['cvc'])
        if charge_res:
            payload = {
                "transaction_id": charge_res,
                "amount": request.data['amount'],
                "created_by": request.user.pk,
                "updated_by": request.user.pk,
                "type": "DR"
            }
            serializer = PaymentHistorySerializer(data=payload)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response({'message': 'Payment is not done.'}, status=status.HTTP_400_BAD_REQUEST)


# 