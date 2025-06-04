from rest_framework import serializers
from .models import ConsortiumMember, Expert, TAFRecord
from users.serializers import UserSerializer # For created_by field

class ConsortiumMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConsortiumMember
        fields = '__all__'

class ExpertSerializer(serializers.ModelSerializer):
    consortium_member_details = ConsortiumMemberSerializer(source='consortium_member', read_only=True)
    class Meta:
        model = Expert
        fields = '__all__'

class TAFRecordSerializer(serializers.ModelSerializer):
    assigned_experts_details = ExpertSerializer(source='assigned_experts', many=True, read_only=True)
    created_by_details = UserSerializer(source='created_by', read_only=True)
    # Use a CharField for themes_list for input, and handle conversion in view or serializer
    themes_list_input = serializers.ListField(
       child=serializers.CharField(), write_only=True, required=False
    )

    class Meta:
        model = TAFRecord
        fields = '__all__' # Or list explicitly
        read_only_fields = ('created_at', 'updated_at', 'created_by')

    def create(self, validated_data):
        themes_input = validated_data.pop('themes_list_input', [])
        # assigned_experts_data = validated_data.pop('assigned_experts', []) # M2M handled after instance creation

        taf_record = TAFRecord.objects.create(**validated_data)
        taf_record.themes_list = themes_input # Use the setter

        # if assigned_experts_data: # If you pass expert IDs in request
        #     taf_record.assigned_experts.set(assigned_experts_data)
        taf_record.save()
        return taf_record

    def update(self, instance, validated_data):
        themes_input = validated_data.pop('themes_list_input', None)
        # assigned_experts_data = validated_data.pop('assigned_experts', None)

        instance = super().update(instance, validated_data)

        if themes_input is not None:
            instance.themes_list = themes_input

        # if assigned_experts_data is not None:
        #     instance.assigned_experts.set(assigned_experts_data)
        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['themes_list'] = instance.themes_list # Add the list representation
        return representation
