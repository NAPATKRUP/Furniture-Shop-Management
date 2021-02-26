from django.urls import path

from . import views

urlpatterns = [
    path('customer/', views.manage_customer, name='manage_customer'),
    path('customer/add/', views.add_customer, name='add_customer'),
    path('customer/edit/<int:id>/', views.edit_customer, name='edit_customer'),
    path('supplier/', views.manage_supplier, name='manage_supplier'),
    path('supplier/add/', views.add_supplier, name='add_supplier'),
    path('supplier/edit/<int:id>/', views.edit_supplier, name='edit_supplier'),
    path('employee/', views.manage_employee, name='manage_employee'),
    path('employee/add/', views.add_employee, name='add_employee'),
    path('employee/edit/<int:id>/', views.edit_employee, name='edit_employee'),
    path('item/', views.manage_item, name='manage_item'),
    path('item/add/', views.add_item, name='add_item'),
    path('item/edit/<int:id>/', views.edit_item, name='edit_item'),
    path('stock/', views.manage_stock, name='manage_stock'),
    path('stock/add/', views.add_stock, name='add_stock'),
    path('stock/edit/<int:id>/', views.edit_stock, name='edit_stock'),
]
