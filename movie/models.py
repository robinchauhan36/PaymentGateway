from django.contrib.auth.models import User
from django.db import models


class CityMaster(models.Model):
    """
    This is a master data for all the city names
    """
    name = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class Movies(models.Model):
    """
    This is a data for all the movie information
    """
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='movie', null=True, blank=True)
    city = models.ForeignKey(CityMaster, on_delete=models.CASCADE)
    date = models.DateField()
    cinema = models.CharField(max_length=128)
    time = models.TimeField()
    total_seats = models.PositiveIntegerField()
    vacant_seats = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class UserBooking(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seats = models.PositiveIntegerField()
    booking_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


