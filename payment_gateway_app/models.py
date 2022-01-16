from django.contrib.auth.models import User
from django.db import models

Card_Type = (
    ('credit_card', 'credit_card'),
    ('debit_card', 'debit_card'),
)

Payment_Status = (
    ('pending', 'pending'),
    ('success', 'success'),
    ('failed', 'failed'),
)


class PaymentDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.CharField(max_length=128, default=0)
    currency = models.CharField(max_length=128, default='')
    type = models.CharField(max_length=128, choices=Card_Type, default='')
    status = models.CharField(max_length=128, choices=Payment_Status, default='pending')
    authorization_code = models.CharField(max_length=128, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
