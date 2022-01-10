from rest_framework.response import Response

from .serializer import CitySerializer, MovieSerializer, UserMovieBookingSerializer, UserMovieBookingListSerializer
from .models import CityMaster, Movies, UserBooking
from rest_framework import generics, permissions, viewsets, views, status
from django_filters.rest_framework import DjangoFilterBackend


# Create your views here.
class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    queryset = CityMaster.objects.all()


class MoviesViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    queryset = Movies.objects.all()
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'city', 'date', 'time', 'cinema']


class UserMovieBookingViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post')
    serializer_class = UserMovieBookingSerializer
    queryset = UserBooking.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        """
        This get API gives you the list of movies booked by user
        """
        queryset = self.filter_queryset(self.get_queryset()).filter(user=request.user)
        serializer = UserMovieBookingListSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        This post request API used to book movies for a particular date, city, time and cinema.
        """
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        vacant_seats = Movies.objects.get(id=data['movie']).vacant_seats
        new_vacant_seats = vacant_seats-int(data['seats'])
        Movies.objects.filter(id=data['movie']).update(vacant_seats=new_vacant_seats)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

