from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Gym
from .serializers import GymListSerializer, GymDetailSerializer


class GymViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for gyms.
    GET /api/v1/gyms/          → list all gyms (paginated)
    GET /api/v1/gyms/{id}/     → single gym detail
    GET /api/v1/gyms/?city=Mumbai  → filter by city
    GET /api/v1/gyms/?search=iron  → search by name
    """
    queryset = Gym.objects.filter(is_active=True)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'state']
    search_fields = ['name', 'city', 'state']
    ordering_fields = ['rating', 'monthly_fee', 'name', 'city']
    ordering = ['city', 'name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return GymDetailSerializer
        return GymListSerializer
