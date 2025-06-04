from rest_framework import viewsets, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Template
from .serializers import TemplateSerializer
from users.permissions import IsAdminUser, CanDownloadAttachment # IsAdminOrReadOnly could be used too

class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all().order_by('-uploaded_at')
    serializer_class = TemplateSerializer
    parser_classes = (MultiPartParser, FormParser) # For file uploads

    def get_permissions(self):
        if self.action in ['list', 'retrieve']: # Allow download/view for authenticated users
            return [CanDownloadAttachment()]
        return [IsAdminUser()] # All other actions (create, update, delete) for admin only

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user, file=self.request.data.get('file'))

    # Add download functionality if needed, or rely on direct file URL access
