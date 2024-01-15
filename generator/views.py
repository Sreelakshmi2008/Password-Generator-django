from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import random
from .serialziers import *
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate

class UserRegistrationView(APIView):
    def post(self, request):
        print(request)
        print(User.objects.all())
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):   
    def post(self, request):
        print(request.data)
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        refresh['username'] = user.username
        refresh['is_superuser'] = user.is_superuser
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)

        return Response({
          
              'user_id': user.id,
              'username':user.username,
              "password": user.password,
              "access": access_token,
              "refresh": refresh_token,
        }, status=status.HTTP_200_OK)


class PasswordGeneratorAPIView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self, request, *args, **kwargs):
        choices = request.data.get('choices', [])
        print(choices)

        if not choices:
            # If choices are empty, generate a random password
            char = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()')
        else:
            # Generate password based on user choices
            char = []
            if 'lowercase' in choices:
                char.extend('abcdefghijklmnopqrstuvwxyz')
               

            if 'uppercase' in choices:
                char.extend('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

            if 'numbers' in choices:
                char.extend('0123456789')

            if 'symbols' in choices:
                char.extend('!@#$%^&*()')
               

        length = int(request.data.get('length', 12))  # Default length is 12 if not provided
        print(length)

        gen_password = ''
        for i in range(length):
            gen_password += random.choice(char)

        return Response({'password': gen_password}, status=status.HTTP_200_OK)
