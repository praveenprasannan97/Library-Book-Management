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
]