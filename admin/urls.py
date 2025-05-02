from django.urls import path
from . import views

app_name = 'admin'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    
    # Products
    path('products/', views.product_list, name='products'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    
    # Categories
    path('categories/', views.category_list, name='categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_category, name='delete_category'),
    
    # Users
    path('users/', views.user_list, name='users'),
    path('users/edit/<int:pk>/', views.edit_user, name='edit_user'),
    path('users/toggle-status/<int:pk>/', views.toggle_user_status, name='toggle_user_status'),
]