from django.urls import path
from userapi import views

urlpatterns = [
    path('signup/', views.api_signup, name='api_signup'),
    path('login/', views.api_login, name='api_login'),
    
]