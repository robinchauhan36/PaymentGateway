from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from django.db.models import signals
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib import messages


# Create your models here.
class Profile(models.Model):
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.FileField(upload_to='user/profile', null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    gender = models.CharField(max_length=25, choices=GENDER, default='Male')
