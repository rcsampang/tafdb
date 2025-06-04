from rest_framework import serializers
from .models import Template
from users.serializers import UserSerializer

class TemplateSerializer(serializers.ModelSerializer):
    uploaded_by_details = UserSerializer(source='uploaded_by', read_only=True)
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Template
        fields = '__all__'
        read_only_fields = ('uploaded_at', 'updated_at', 'uploaded_by', 'file_url')

    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None
