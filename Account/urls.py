from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('start/', views.let_start, name='start'),
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
    path('change_password/', views.change_password, name='change_password'),
]
