from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view , permission_classes
from rest_framework.authtoken.models import Token
from rest_framework import status, exceptions, authentication
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User, Group
from .serializers import UserSerializer, AuthorSerializer, AuthorSerializer2, BookSerializer, BookSerializer2, BorrowingHistorySerializer, BorrowingHistorySerializer2
from .models import Author, Book, BorrowingHistory





@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def api_signup(request):

    is_staff = request.data.get('is_staff', False)

    if is_staff:
        if request.user.is_staff:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user_data = serializer.validated_data
                user = serializer.save()
                user.password = make_password(user_data['password'])
                user.is_staff = True
                admin_group, created = Group.objects.get_or_create(name='admin')
                user.groups.add(admin_group)
                user.save()
                return Response({'message': 'New Account Created'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Invalid data', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(
                {'error': 'Permission denied. Only staff members can create admin accounts.'},
                status=status.HTTP_403_FORBIDDEN
            )
    else:
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data

            user = serializer.save()
            user.password = make_password(user_data['password'])
            user.is_staff = False

            user_group, created = Group.objects.get_or_create(name='user')
            user.groups.add(user_group)
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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_logout(request):

    user = request.user
    token = Token.objects.get(user=user)
    token.delete()
    return Response(status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_home(request):

    user = request.user
    if user.groups.filter(name='admin').exists():
        print("User is an admin")
    return Response(status=status.HTTP_200_OK)


@api_view(['DELETE','POST','PUT', 'GET'])
@permission_classes([IsAuthenticated])
def api_add_author(request, id):
    
    if request.method == 'POST':
        if request.user.has_perm('userapi.can_add_author'):
            serializer = AuthorSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'GET':
        if request.user.has_perm('userapi.can_list_author'):
            author = Author.objects.get(id=id)
            serializer = AuthorSerializer(author)
            return Response(serializer.data)
        else:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'PUT':
        if request.user.has_perm('userapi.can_edit_author'):
            author = Author.objects.get(id=id)
            serializer = AuthorSerializer(author, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    elif request.method == 'DELETE':
        if request.user.has_perm('userapi.can_delete_author'):
            author = Author.objects.get(id=id)
            author.delete()
            return Response({'message': 'Author deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_list_authors(request):
    if request.user.has_perm('userapi.can_list_author'):
        authors = Author.objects.all()
        serializer = AuthorSerializer2(authors, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_profile(request):
    user = request.user
    groups = user.groups.values_list('name', flat=True)
    profile_data = {
        'username': user.username,
        'email': user.email,
        'group': groups[0] if groups else 'No group'
    }
    return Response(profile_data, status=status.HTTP_200_OK)

@api_view(['DELETE','POST','PUT', 'GET'])
@permission_classes([IsAuthenticated])
def api_books(request, id):
    if request.method == 'POST':
        if request.user.has_perm('userapi.can_add_book'):
            serializer = BookSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'DELETE':
        if request.user.has_perm('userapi.can_delete_book'):
            book = get_object_or_404(Book, id=id)
            book.delete()
            return Response({'message': 'Book deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'GET':
        if request.user.has_perm('userapi.can_list_book'):
            book = get_object_or_404(Book, id=id)
            serializer = BookSerializer2(book)
            return Response(serializer.data)
        else:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    if request.method == 'PUT':
        if request.user.has_perm('userapi.can_edit_book'):
            book = get_object_or_404(Book, id=id)
            serializer = BookSerializer(book, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_list_books(request):
    if request.user.has_perm('userapi.can_list_book'):
        books = Book.objects.all()
        serializer = BookSerializer2(books, many=True)
        return Response(serializer.data)
    else:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def api_borrow_book(request, id):
    user = request.user
    book = get_object_or_404(Book, id=id)
    if request.user.has_perm('userapi.can_borrow_book'):
        if book.copies_available > 0:
            book.copies_available -= 1
            if book.copies_available == 0:
                book.status = 'borrowed'
            book.save()

            BorrowingHistory.objects.create(
                book=book,
                user=user,
                borrow_date=timezone.now(),
                status='borrowed'
            )

            return Response({'message': 'Book borrowed successfully', 'book': book.title}, status=status.HTTP_200_OK)
        
        return Response({'error': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_my_borrowing(request):
    user = request.user
    if request.user.has_perm('userapi.can_view_history'):
        borrow_history = BorrowingHistory.objects.filter(user=user)
        serializer = BorrowingHistorySerializer(borrow_history, many=True)
        return Response(serializer.data)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def api_return_book(request, id):
    user = request.user
    borrow_entry = get_object_or_404(BorrowingHistory, id=id, user=user, status='borrowed')
    book = borrow_entry.book
    
    if request.user.has_perm('userapi.can_return_book'):
        book.copies_available += 1
        book.status = 'available'
        book.save()

        borrow_entry.return_date = timezone.now()
        borrow_entry.status = 'returned'
        borrow_entry.save()

        return Response({'message': 'Book returned successfully', 'book': book.title}, status=status.HTTP_200_OK)

    return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_borrowing_history(request):
    if request.user.has_perm('userapi.can_view_history'):
        borrowing_history = BorrowingHistory.objects.all()
        serializer = BorrowingHistorySerializer2(borrowing_history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Permission denied'}, status=status.HTTP_403_FORBIDDEN)