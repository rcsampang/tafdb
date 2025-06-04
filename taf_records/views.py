from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import ConsortiumMember, Expert, TAFRecord
from .serializers import ConsortiumMemberSerializer, ExpertSerializer, TAFRecordSerializer
from users.permissions import IsAdminUser, IsAdminOrReadOnly # Import custom permissions

class ConsortiumMemberViewSet(viewsets.ModelViewSet):
    queryset = ConsortiumMember.objects.all().order_by('-created_at')
    serializer_class = ConsortiumMemberSerializer
    permission_classes = [IsAdminUser] # Only admin can manage

class ExpertViewSet(viewsets.ModelViewSet):
    queryset = Expert.objects.all().order_by('name')
    serializer_class = ExpertSerializer
    permission_classes = [IsAdminUser] # Only admin can manage
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'email', 'expertise']

class TAFRecordViewSet(viewsets.ModelViewSet):
    queryset = TAFRecord.objects.all().order_by('-created_at')
    serializer_class = TAFRecordSerializer
    permission_classes = [IsAdminOrReadOnly] # Admin R/W, Authenticated ReadOnly
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]

    # Fields for DjangoFilterBackend
    filterset_fields = {
        'country': ['exact', 'in'],
        'scope': ['exact', 'in'],
        'type_of_ta': ['exact', 'in'],
        'start_date': ['gte', 'lte', 'exact'],
        'end_date': ['gte', 'lte', 'exact', 'isnull'],
        'experts_involved_flag': ['exact'],
        'assigned_experts__id': ['exact'], # Filter by expert ID
        'assigned_experts__name': ['icontains'],
        'themes_text': ['icontains'], # Search in the comma-separated themes string
    }
    search_fields = ['title', 'area', 'location', 'remarks', 'experts_details_text', 'themes_text']
    ordering_fields = ['start_date', 'end_date', 'country', 'title', 'created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
