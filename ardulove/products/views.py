from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def product_list(request):

    category = request.GET.get('category')
    if category:
        products = Product.objects.filter(categories__id=category).order_by('-id')
    else:
        products = Product.objects.all().order_by('-id')

    category = Category.objects.all()

    return render(request, 'products/products.html', {'products': products, 'categories': category})

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'products/product_detail.html', {'product': product})
