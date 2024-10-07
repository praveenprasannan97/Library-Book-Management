from django.urls import path
from userapi import views

urlpatterns = [
    path('signup/', views.api_signup, name='api_signup'),
    path('login/', views.api_login, name='api_login'),
    path('logout/', views.api_logout, name='api_logout'),
    path('home/', views.api_home, name='api_home'),
    path('authors/<int:id>/', views.api_add_author, name='api_add_author'),
    path('listauthors/', views.api_list_authors, name='api_list_authors'),
    path('profile/', views.api_profile, name='api_profile'),
    path('books/<int:id>/', views.api_books, name='api_books'),
    path('books/', views.api_list_books, name='api_list_books'),
    path('books/<int:id>/borrow/', views.api_borrow_book, name='api_borrow_book'),
    path('books/<int:id>/return/', views.api_return_book, name='api_return_book'),
    path('my_borrowing/', views.api_my_borrowing, name='api_my_borrowing'),
    path('borrowinghistory/', views.api_borrowing_history, name='api_borrowing_history'),
]