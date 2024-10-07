from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Author, Book, BorrowingHistory

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

class BookSerializer(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)

    class Meta:
        model = Book
        fields = ['title', 'ISBN', 'authors', 'publication_date', 'copies_available', 'status']

    def create(self, validated_data):
        authors_data = validated_data.pop('authors')
        book = Book.objects.create(**validated_data)
        book.authors.set(authors_data)
        return book

    def update(self, instance, validated_data):
        authors_data = validated_data.pop('authors', None)
        instance.title = validated_data.get('title', instance.title)
        instance.ISBN = validated_data.get('ISBN', instance.ISBN)
        instance.publication_date = validated_data.get('publication_date', instance.publication_date)
        instance.copies_available = validated_data.get('copies_available', instance.copies_available)
        instance.status = validated_data.get('status', instance.status)

        if authors_data is not None:
            instance.authors.set(authors_data)
        
        instance.save()
        return instance
    
class BookSerializer2(serializers.ModelSerializer):
    authors = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all(), many=True)

    class Meta:
        model = Book
        fields = ['id','title', 'ISBN', 'authors', 'publication_date', 'copies_available', 'status']


class BorrowingHistorySerializer(serializers.ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = BorrowingHistory
        fields = ['id', 'book', 'borrow_date', 'return_date', 'status']

class BorrowingHistorySerializer2(serializers.ModelSerializer):
    book = BookSerializer()
    user = UserSerializer()

    class Meta:
        model = BorrowingHistory
        fields = ['id', 'book', 'user', 'borrow_date', 'status', 'return_date']