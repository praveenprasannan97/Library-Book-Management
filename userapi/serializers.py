from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_staff']

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['name', 'date_of_birth', 'country']

class AuthorSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'date_of_birth', 'country']