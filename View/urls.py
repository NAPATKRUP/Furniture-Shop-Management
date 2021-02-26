from django.urls import path

from . import views

urlpatterns = [
    path('supplier/', views.view_supplier, name='view_supplier'),
    path('stock/', views.view_stock, name='view_stock'),
    path('history/', views.view_history, name='view_history'),
    path('order/<int:id>/', views.view_order, name='view_order')
]
