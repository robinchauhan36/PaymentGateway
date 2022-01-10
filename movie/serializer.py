from rest_framework import serializers, exceptions
from .models import *


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CityMaster
        fields = '__all__'


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = '__all__'


class UserMovieBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBooking
        fields = '__all__'


class UserMovieBookingListSerializer(serializers.ModelSerializer):
    movie = MovieSerializer()

    class Meta:
        model = UserBooking
        fields = '__all__'