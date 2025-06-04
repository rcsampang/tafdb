from rest_framework import serializers
from .models import Attachment
from users.serializers import UserSerializer

class AttachmentSerializer(serializers.ModelSerializer):
    uploaded_by_details = UserSerializer(source='uploaded_by', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Attachment
        fields = '__all__'
        read_only_fields = ('uploaded_at', 'uploaded_by', 'file_name', 'file_url')

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
