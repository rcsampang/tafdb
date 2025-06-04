from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('user_type', 'bio') # Add other fields as needed

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True) # Read-only nested profile
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'profile')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # UserProfile is created by signal
        return user

class RegisterSerializer(serializers.ModelSerializer):
    profile_user_type = serializers.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES, write_only=True, required=False, default='regular')

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name', 'profile_user_type')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_type = validated_data.pop('profile_user_type', 'regular')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        # UserProfile is created by signal, then we update its type
        user.profile.user_type = user_type
        user.profile.save()
        return user
