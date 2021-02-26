from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('create_order/', views.create_order, name='create_order'),
    path('send_order/', views.send_order, name='send_order'),
    path('show_status/', views.show_status, name='show_status')
]
