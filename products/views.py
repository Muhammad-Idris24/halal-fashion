from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from .forms import  ContactForm

def home(request):
    featured_products = Product.objects.filter(available=True)[:8]
    categories = Category.objects.all()[:6]
    return render(request, 'products/home.html', {
        'featured_products': featured_products,
        'categories': categories,
    })

def about(request):
    return render(request, 'products/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process form data
            return redirect('products:contact_success')
    else:
        form = ContactForm()
    return render(request, 'products/contact.html', {'form': form})

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    return render(request, 'products/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'products/detail.html', {'product': product})