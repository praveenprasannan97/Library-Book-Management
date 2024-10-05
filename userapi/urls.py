from django.urls import path
from userapi import views

urlpatterns = [
    path('signup/', views.api_signup, name='api_signup'),
    path('login/', views.api_login, name='api_login'),
    path('home/', views.api_home, name='api_home'),
    path('authors/<int:id>/', views.api_add_author, name='api_add_author'),
    path('listauthors/', views.api_list_authors, name='api_list_authors'),
]