from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from products.models import Product, Category
from products.forms import ProductForm, CategoryForm
from accounts.models import CustomUser
from accounts.forms import UserEditForm

def admin_check(user):
    """Check if user is admin"""
    return user.is_authenticated and user.is_admin

# Dashboard View
@user_passes_test(admin_check, login_url='/accounts/login/')
def dashboard(request):
    context = {
        'products_count': Product.objects.count(),
        'categories_count': Category.objects.count(),
        'users_count': CustomUser.objects.count(),
        'recent_products': Product.objects.order_by('-created')[:5],
        'recent_users': CustomUser.objects.order_by('-date_joined')[:5]
    }
    return render(request, 'admin/dashboard.html', context)

# ============== PRODUCT VIEWS ==============
@user_passes_test(admin_check, login_url='/accounts/login/')
def product_list(request):
    products = Product.objects.all().order_by('-created')
    
    # Pagination
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        products = products.filter(name__icontains=search_query)
        page_obj = products
    
    form = ProductForm()
    return render(request, 'admin/products/list.html', {
        'products': page_obj,
        'product_form': form,
        'search_query': search_query or ''
    })

@user_passes_test(admin_check, login_url='/accounts/login/')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" added successfully!')
            return redirect('admin:products')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
    
    return render(request, 'admin/products/add.html', {'form': form})

@user_passes_test(admin_check, login_url='/accounts/login/')
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Product "{product.name}" updated successfully!')
            return redirect('admin:products')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'admin/products/edit.html', {
        'form': form,
        'product': product
    })

@user_passes_test(admin_check, login_url='/accounts/login/')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product_name = product.name
        product.delete()
        messages.success(request, f'Product "{product_name}" deleted successfully!')
        return redirect('admin:products')
    
    return render(request, 'admin/products/confirm_delete.html', {'product': product})

# ============== CATEGORY VIEWS ==============
@user_passes_test(admin_check, login_url='/accounts/login/')
def category_list(request):
    categories = Category.objects.all().order_by('name')
    form = CategoryForm()
    return render(request, 'admin/categories/list.html', {
        'categories': categories,
        'form': form
    })

@user_passes_test(admin_check, login_url='/accounts/login/')
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" added successfully!')
            return redirect('admin:categories')
    else:
        form = CategoryForm()
    
    return render(request, 'admin/categories/add.html', {'form': form})

@user_passes_test(admin_check, login_url='/accounts/login/')
def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Category "{category.name}" updated successfully!')
            return redirect('admin:categories')
    else:
        form = CategoryForm(instance=category)
    
    return render(request, 'admin/categories/edit.html', {
        'form': form,
        'category': category
    })

@user_passes_test(admin_check, login_url='/accounts/login/')
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category_name = category.name
        category.delete()
        messages.success(request, f'Category "{category_name}" deleted successfully!')
        return redirect('admin:categories')
    
    return render(request, 'admin/categories/confirm_delete.html', {'category': category})

# ============== USER VIEWS ==============
@user_passes_test(admin_check, login_url='/accounts/login/')
def user_list(request):
    users = CustomUser.objects.all().order_by('-date_joined')
    
    # Filter by user type
    user_type = request.GET.get('type')
    if user_type in ['1', '2']:
        users = users.filter(user_type=user_type)
    
    return render(request, 'admin/users/list.html', {
        'users': users,
        'user_type': user_type or 'all'
    })

@user_passes_test(admin_check, login_url='/accounts/login/')
def edit_user(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User "{user.email}" updated successfully!')
            return redirect('admin:users')
    else:
        form = UserEditForm(instance=user)
    
    return render(request, 'admin/users/edit.html', {
        'form': form,
        'user': user
    })

@user_passes_test(admin_check, login_url='/accounts/login/')
def toggle_user_status(request, pk):
    user = get_object_or_404(CustomUser, pk=pk)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        status = "activated" if user.is_active else "deactivated"
        messages.success(request, f'User "{user.email}" has been {status}.')
    
    return redirect('admin:users')