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

from django.core import management
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.permissions import IsAdminUser # Make sure this is correctly importable
import os
from django.conf import settings
from django.http import FileResponse, Http404

class TriggerBackupDatabaseAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        try:
            management.call_command('backup_database')
            return Response({'message': 'Database backup process initiated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Failed to initiate database backup: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TriggerBackupApplicationAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        try:
            management.call_command('backup_application')
            return Response({'message': 'Application backup process initiated successfully.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Failed to initiate application backup: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ListBackupsAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        backup_base_dir = os.path.join(settings.BASE_DIR, 'backups')
        backups = {'database': [], 'application': []}

        db_backup_dir = os.path.join(backup_base_dir, 'database')
        if os.path.exists(db_backup_dir):
            backups['database'] = sorted([f for f in os.listdir(db_backup_dir) if os.path.isfile(os.path.join(db_backup_dir, f))], reverse=True)

        app_backup_dir = os.path.join(backup_base_dir, 'application')
        if os.path.exists(app_backup_dir):
            backups['application'] = sorted([f for f in os.listdir(app_backup_dir) if os.path.isfile(os.path.join(app_backup_dir, f))], reverse=True)

        return Response(backups, status=status.HTTP_200_OK)

class DownloadBackupAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, type, filename, *args, **kwargs):
        # Basic path traversal prevention
        if '..' in filename or filename.startswith('/'):
            return Response({'error': 'Invalid filename.'}, status=status.HTTP_400_BAD_REQUEST)

        backup_dir = os.path.join(settings.BASE_DIR, 'backups', type)
        filepath = os.path.join(backup_dir, filename)

        if not os.path.exists(filepath) or not os.path.isfile(filepath):
            raise Http404('Backup file not found.')

        try:
            return FileResponse(open(filepath, 'rb'), as_attachment=True, filename=filename)
        except Exception as e:
            return Response({'error': f'Error serving file: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
