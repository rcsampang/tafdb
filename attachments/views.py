from rest_framework import viewsets, status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse, Http404
from .models import Attachment
from .serializers import AttachmentSerializer
from users.permissions import IsAdminUser, CanDownloadAttachment

class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all().order_by('-uploaded_at')
    serializer_class = AttachmentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'download']: # Allow view/download for authenticated
            return [CanDownloadAttachment()]
        return [IsAdminUser()] # Create, update, delete for admin only

    def perform_create(self, serializer):
        # Ensure file is passed correctly
        serializer.save(uploaded_by=self.request.user, file=self.request.data.get('file'))

    @action(detail=True, methods=['get'], permission_classes=[CanDownloadAttachment])
    def download(self, request, pk=None):
        try:
            attachment = self.get_object()
            # In a real scenario, consider serving files via Nginx X-Accel-Redirect or similar for large files
            # For now, use Django's FileResponse for simplicity
            file_handle = attachment.file.open()
            response = FileResponse(file_handle, as_attachment=True, filename=attachment.file_name)
            return response
        except FileNotFoundError:
            raise Http404('File not found.')
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
