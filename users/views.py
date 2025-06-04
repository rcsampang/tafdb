from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserSerializer, RegisterSerializer
from django.contrib.auth.models import User

class UserRegistrationAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (permissions.AllowAny,) # Anyone can register

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user).data # Use UserSerializer to include profile
        return Response({
            'user': user_data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)

class CustomAuthTokenLoginAPIView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user).data # Use UserSerializer to include profile
        return Response({
            'token': token.key,
            'user': user_data
        })

class UserLogoutAPIView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        try:
            # Simply delete the token on logout
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass # Token already deleted or never existed
        logout(request) # Django's session logout, good practice
        return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)

class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user # Return current authenticated user
