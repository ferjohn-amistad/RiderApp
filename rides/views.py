from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Prefetch
from datetime import timedelta

from .models import Ride, RideEvent, User
from .serializers import RideSerializer, UserSerializer
from .permissions import IsAdminRole
from .filters import RideFilter



class RideViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminRole]
    serializer_class = RideSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RideFilter
    ordering_fields = ['pickup_time']


    def get_queryset(self):
        last_24_hours = timezone.now() - timedelta(hours=24)
        todays_events = RideEvent.objects.filter(
            created_at__gte=last_24_hours
        )

        return Ride.objects.prefetch_related(
            Prefetch('ride_events', queryset=todays_events, to_attr='todays_ride_events'),
            ).select_related('id_rider', 'id_driver')


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()