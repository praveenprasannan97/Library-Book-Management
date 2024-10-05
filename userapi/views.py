from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view , permission_classes
from rest_framework.authtoken.models import Token
from rest_framework import status, exceptions, authentication
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserSerializer





@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def api_signup(request):

    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():

        user_data = serializer.validated_data


        user = serializer.save()
        user.password = make_password(user_data['password'])
        user.is_staff = False
        user.save()
        
        return Response({'message': 'New Account Created'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Invalid data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def api_login(request):

    username = request.data.get('username')
    password = request.data.get('password')
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)

    if not user:
        return Response({'error': 'Invalid Credentials'},status=status.HTTP_404_NOT_FOUND)
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},status=status.HTTP_200_OK)